# Copyright 2019 Google LLC
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

import hashid

json_edge = {
    'color': {
        'color': '#A7A7A7'
    },
    'title': 'JSON Parsing Functions',
    'label': 'HAsh'
}


def run(unfurl, node):

    if node.data_type in ('url.query.pair', 'string'):

        x = hashid.HashID()
        y = x.identifyHash(node.value)

        for item in y:
            print(item)
            print(item.name)

        unfurl.add_to_queue(
            data_type='json', key=y, value=y,
            hover='This was parsed as JavaScript Object Notation (JSON), <br>'
                  'which uses human-readable text to store and transmit data objects',
            parent_id=node.node_id, incoming_edge_config=json_edge)

