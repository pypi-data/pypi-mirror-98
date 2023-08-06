# Copyright 2019 Dan Nemec
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

import urllib.parse
import warnings

try:
    from publicsuffix2 import PublicSuffixList
    psl = PublicSuffixList(idna=False)
except ImportError:
    warnings.warn("Unable to import the nodule 'publicsuffix2'. "
                  "Will be unable to parse domain names.")
    psl = None


urlparse_edge = {
    'color': {
        'color': '#4d4d4d'
    },
    'title': 'URL Parsing Functions',
    'label': 'u'
}


def run(unfurl, node):
    if psl is None or node.data_type != 'url.hostname' or not isinstance(node.value, str):
        return

    full_domain = node.value
    if full_domain.startswith('xn--') or '.xn--' in full_domain:
        # punycoded domain
        full_domain = full_domain.encode('utf8').decode('idna')
    if '%' in full_domain:
        # percent-encoded domain
        full_domain = urllib.parse.unquote(full_domain)

    domain = psl.get_sld(full_domain)
    if domain is not None:
        if len(domain) != len(full_domain):
            subdomain = full_domain[:-len(domain)-1]
            unfurl.add_to_queue(
                data_type='url.subdomain', key='Subdomain', value=subdomain,
                hover='This is the <b>sub-domain</b> part of the domain or netloc.',
                parent_id=node.node_id, incoming_edge_config=urlparse_edge)
        unfurl.add_to_queue(
            data_type='url.domain', key='Domain Name', value=domain,
            hover='This is the base, registerable, part of the domain or netloc',
            parent_id=node.node_id, incoming_edge_config=urlparse_edge)
        
    tld = psl.get_tld(full_domain)
    if tld is not None:
        unfurl.add_to_queue(
            data_type='url.tld', key='TLD', value=tld,
            hover='This is the <b>Top Level Domain</b>, or TLD, for the domain or netloc',
            parent_id=node.node_id, incoming_edge_config=urlparse_edge)
