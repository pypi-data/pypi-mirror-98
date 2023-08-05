#!/usr/bin/env python3

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import configparser
import importlib
import networkx
import queue
import re
import unfurl.parsers
from flask import Flask, render_template, request
from flask_cors import CORS

import logging
log = logging.getLogger(__name__)


class Unfurl:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.queue = queue.Queue()
        self.next_id = 1
        self.graph = networkx.DiGraph()
        self.total_nodes = 0
        self.api_keys = {}

        config = configparser.ConfigParser()
        config.read('unfurl.ini')
        if config.has_section('API_KEYS'):
            self.api_keys = config['API_KEYS']

    class Node:
        def __init__(self, node_id, data_type, key, value, label=None, hover=None,
                     parent_id=None, incoming_edge_config=None, extra_options=None):
            self.node_id = node_id
            self.data_type = data_type
            self.key = key
            self.value = value
            self.label = label
            self.hover = hover
            self.parent_id = parent_id
            self.incoming_edge_config = incoming_edge_config
            self.extra_options = extra_options

            if self.label is None:
                if self.key and self.value:
                    self.label = f'{self.key}: {self.value}'
                elif self.value:
                    self.label = self.value

        def __repr__(self):
            return str(self.__dict__)

    def get_predecessor_node(self, node):
        if not node.parent_id:
            return False
        predecessor = list(self.graph.predecessors(node))
        assert len(predecessor) == 1
        return predecessor[0]

    def get_successor_nodes(self, node):
        successors = list(self.graph.successors(node))
        return successors

    def check_sibling_nodes(self, node, data_type=None, key=None, value=None):
        parent_node = self.get_predecessor_node(node)

        if not parent_node:
            return False

        assert type(parent_node) == Unfurl.Node, \
            f'Expected Unfurl.Node as parent type; got {type(parent_node)}'

        sibling_nodes = self.get_successor_nodes(parent_node)

        for sibling_node in sibling_nodes:

            # Skip the "sibling" if it's actually the source node
            if node.node_id == sibling_node.node_id:
                continue

            # For each attribute, check if it is set. If it is and it
            # doesn't match, stop checking this node and go to the next
            if data_type and data_type != sibling_node.data_type:
                continue
            if key and key != sibling_node.key:
                continue
            if value and value != sibling_node.value:
                continue

            # This node matched all the given criteria;
            return True

        # If we got here, no nodes matched all criteria.
        return False

    def find_preceding_domain(self, node):
        parent_node = self.get_predecessor_node(node)

        if not parent_node:
            return ''

        assert isinstance(parent_node, Unfurl.Node), \
            f'Expected Unfurl.Node as parent type; got {type(parent_node)}'

        if parent_node.data_type == 'url.hostname':
            assert isinstance(parent_node.value, str)
            return parent_node.value
        elif parent_node.data_type == 'url':
            for child_node in self.get_successor_nodes(parent_node):
                if child_node.data_type == 'url.hostname':
                    assert isinstance(child_node.value, str)
                    return child_node.value
                elif child_node.data_type == 'url.authority':
                    for subcomponent in self.get_successor_nodes(child_node):
                        if subcomponent.data_type == 'url.hostname':
                            assert isinstance(subcomponent.value, str)
                            return subcomponent.value
            return ''
        else:
            return self.find_preceding_domain(parent_node)

    def get_id(self):
        new_id = self.next_id
        self.next_id += 1
        return new_id

    def create_node(
            self, data_type, key, value, label, hover, parent_id=None,
            incoming_edge_config=None, extra_options=None):
        new_node = self.Node(
            self.get_id(), data_type=data_type, key=key, value=value,
            label=label, hover=hover, parent_id=parent_id,
            incoming_edge_config=incoming_edge_config,
            extra_options=extra_options)
        assert new_node.node_id not in self.nodes.keys()
        self.nodes[new_node.node_id] = new_node
        self.graph.add_node(new_node)
        self.total_nodes += 1

        if parent_id:
            self.graph.add_edge(self.nodes[parent_id], new_node)

        return new_node.node_id

    @staticmethod
    def add_b64_padding(encoded_string):
        remainder = len(encoded_string) % 4
        if remainder == 2:
            return f'{encoded_string}=='
        elif remainder == 3:
            return f'{encoded_string}='
        else:
            return encoded_string

    @staticmethod
    def check_if_int_between(value, low, high):
        try:
            value = int(value)
        except:
            return False

        if low < value < high:
            return True
        else:
            return False

    def add_to_queue(
            self, data_type, key, value, label=None, hover=None,
            parent_id=None, incoming_edge_config=None, extra_options=None):
        new_item = {
            'data_type': data_type,
            'key': key,
            'value': value,
            'label': label,
            'hover': hover,
            'incoming_edge_config': incoming_edge_config,
            'extra_options': extra_options
        }

        if parent_id:
            new_item['parent_id'] = parent_id

        if not extra_options:
            max_row_length = len(str(value)) * 2.2
            new_item['extra_options'] = \
                {'widthConstraint': {'maximum': max(max_row_length, 200)}}

        log.info(f'Added to queue: {new_item}')
        self.queue.put(new_item)

    def run_plugins(self, node):

        for unfurl_parser in unfurl.parsers.__all__:
            try:
                parser = importlib.import_module(f'unfurl.parsers.{unfurl_parser}')
            except ImportError as e:
                log.exception(f'Failed to import {unfurl_parser}: {e}')
                continue

            try:
                parser.run(self, node)
            except Exception as e:
                log.exception(f'Exception in {unfurl_parser}: {e}')

    def parse(self, queued_item):
        item = queued_item
        node_id = self.create_node(
            data_type=item['data_type'], key=item['key'], value=item['value'],
            label=item['label'], hover=item['hover'],
            parent_id=item.get('parent_id', None),
            incoming_edge_config=item.get('incoming_edge_config', None),
            extra_options=item.get('extra_options', None))

        if item.get('parent_id'):
            self.get_predecessor_node(self.nodes[node_id])

        self.run_plugins(self.nodes[node_id])

    def parse_queue(self):
        while not self.queue.empty() and self.total_nodes < 100:
            self.parse(self.queue.get())

    @staticmethod
    def transform_node(node):
        transformed = {
            'id': int(node.node_id),
            'label': f'{node.label}'
        }
        if node.hover:
            transformed['title'] = node.hover
        if node.extra_options:
            transformed.update(node.extra_options)
        return transformed

    @staticmethod
    def transform_edge(edge):
        transformed = {
            'from': int(edge[0].node_id),
            'to': int(edge[1].node_id)
        }

        if edge[1].incoming_edge_config:
            transformed.update(edge[1].incoming_edge_config)
        return transformed

    def generate_json(self):
        data_json = {'nodes': [], 'edges': []}
        for orig_node in self.graph.nodes():
            data_json['nodes'].append(self.transform_node(orig_node))
        for orig_edge in self.graph.edges():
            data_json['edges'].append(self.transform_edge(orig_edge))

        edge_summary = {}
        for edge in data_json.get('edges'):
            edge_summary.setdefault(edge.get('title'), 0)
            edge_summary[edge.get('title')] += 1

        data_json['summary'] = edge_summary

        return data_json

    @staticmethod
    def transform_3d_node(node):
        def val_func(node_id):
            if node_id == 1:
                return 15
            elif node_id < 10:
                return 10
            else:
                return 5

        def shorten_name(node_string):
            node_string = str(node_string)
            if len(node_string) > 60:
                return f'{node_string[:25]}...{node_string[-25:]}'
            else:
                return node_string

        node_color = '#aabfad'
        if node.incoming_edge_config:
            if node.incoming_edge_config['color']:
                node_color = node.incoming_edge_config['color']['color']

        transformed = {
                'id': str(node.node_id),
                'name': shorten_name(node.label),
                'fullName': f'{node.label}',
                'dataType': f'{node.data_type}',
                'val': val_func(node.node_id),
                'color': node_color
        }

        if node.hover:
            transformed['description'] = re.sub(r'<.*?>|\[.*?\]', '', node.hover)

        return transformed

    @staticmethod
    def transform_3d_edge(edge):
        transformed = {
            'source': str(edge[0].node_id),
            'target': str(edge[1].node_id)
        }

        if edge[1].incoming_edge_config:
            transformed.update(edge[1].incoming_edge_config)

        if transformed.get('color', {}).get('color'):
            transformed['color'] = transformed['color']['color']
        return transformed

    def generate_3d_json(self):
        data_json = {'nodes': [], 'links': []}
        for orig_node in self.graph.nodes():
            data_json['nodes'].append(self.transform_3d_node(orig_node))
        for orig_edge in self.graph.edges():
            data_json['links'].append(self.transform_3d_edge(orig_edge))
        return data_json

    def generate_text_tree(self, detailed=False, output_filter=None):
        tree_root = None
        for node_contents in self.graph.nodes(data=True):
            # Get the root node; id is 1. Needed for networkx tree_data().
            if node_contents[0].__dict__.get('node_id') == 1:
                tree_root = node_contents[0]
                break

        tree_data = networkx.readwrite.json_graph.tree_data(
            self.graph, root=tree_root)
        output_tree = Unfurl.text_tree(tree_data, detailed=detailed)

        if output_filter:
            filtered_tree = ''
            for line in output_tree.splitlines():
                if re.search(output_filter, line):
                    filtered_tree += f'\n{line}'
            output_tree = filtered_tree

        return output_tree

    @staticmethod
    def text_tree(tree_data, indent='', last_child=False, text_output='', detailed=False):

        node = tree_data['id']
        label = re.sub(r'\n', ' ', str(node.label))

        if node.node_id == 1:
            # This is the root node; don't indent to save space
            text_output += f'[{node.node_id}] {label}'
            if detailed:
                text_output += f' (type: {node.data_type})'
                if node.hover:
                    hover = re.sub(r'<.*?>|\[.*?\]', '', node.hover)
                    text_output += f' -- {hover}'

            indent += ' '

        elif not last_child:
            text_output += f'\n{indent}├─({node.incoming_edge_config["label"]})─[{node.node_id}] {label}'
            if detailed:
                text_output += f' (type: {node.data_type})'
                if node.hover:
                    hover = re.sub(r'<.*?>|\[.*?\]', '', node.hover)
                    text_output += f' -- {hover}'

            indent += '|  '
        else:
            text_output += f'\n{indent}└─({node.incoming_edge_config["label"]})─[{node.node_id}] {label}'
            if detailed:
                text_output += f' (type: {node.data_type})'
                if node.hover:
                    hover = re.sub(r'<.*?>|\[.*?\]', '', node.hover)
                    text_output += f' -- {hover}'

            indent += '   '

        if tree_data.get('children'):
            children_text_output = ''
            for number, child in enumerate(tree_data['children']):
                last_child = \
                    True if (number + 1) == len(tree_data['children']) else False
                children_text_output += \
                    Unfurl.text_tree(
                        child, indent=indent, last_child=last_child, detailed=detailed)
            text_output += children_text_output

        return text_output


unfurl_app_host = None
unfurl_app_port = None
app = Flask(__name__)
CORS(app)


class UnfurlApp:
    def __init__(self, unfurl_debug='True', unfurl_host='localhost', unfurl_port='5000'):
        self.unfurl_debug = unfurl_debug
        self.unfurl_host = unfurl_host
        self.unfurl_port = unfurl_port

        global unfurl_app_host
        global unfurl_app_port
        unfurl_app_host = unfurl_host
        unfurl_app_port = unfurl_port

        app.run(debug=unfurl_debug, host=unfurl_host, port=unfurl_port)


@app.route('/')
def index():
    return render_template(
        'graph.html', url_to_unfurl='', unfurl_host=unfurl_app_host,
        unfurl_port=unfurl_app_port)


@app.route('/<path:url_to_unfurl>')
def graph(url_to_unfurl):
    return render_template(
        'graph.html', url_to_unfurl=url_to_unfurl,
        unfurl_host=unfurl_app_host, unfurl_port=unfurl_app_port)


@app.route('/api/<path:api_path>')
def api(api_path):
    # Get the referrer from the request, which has the full url + query string.
    # Split off the local server and keep just the url we want to parse
    unfurl_this = request.referrer.split(f':{unfurl_app_port}/', 1)[1]

    unfurl_instance = Unfurl()
    unfurl_instance.add_to_queue(
        data_type='url', key=None,
        extra_options={'widthConstraint': {'maximum': 1200}},
        value=unfurl_this)
    unfurl_instance.parse_queue()

    unfurl_json = unfurl_instance.generate_json()
    return unfurl_json
