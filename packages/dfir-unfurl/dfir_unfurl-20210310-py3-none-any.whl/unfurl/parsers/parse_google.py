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

import base64
import datetime
import struct
import pycountry
from unfurl.parsers.proto.google_search_pb2 import Ved
from google.protobuf import json_format

google_edge = {
    'color': {
        'color': 'green'
    },
    'title': 'Google-related Parsing Functions',
    'label': 'G'
}

known_sources = {
    'hp': 'Home Page',
    'serp': 'Search Engine Results Page',
    'img': 'Image Search',
    'psy-ab': 'Address Bar',
    'hangouts': 'Hangouts Chat'
}


def decode_varint(source):
    result = 0
    number_of_bytes = 0
    for read in source:
        result |= ((read & 0x7F) << (number_of_bytes * 7))
        number_of_bytes += 1
        if (read & 0x80) != 0x80:
            return result, number_of_bytes


def parse_ei(ei):
    """Parse ei parameters from Google searches.

    Based on work by:
      Adrian Leong (cheeky4n6monkey@gmail.com) -
        https://github.com/cheeky4n6monkey/4n6-scripts/blob/master/google-ei-time.py
      Kevin Jones - https://deedpolloffice.com/blog/articles/decoding-ei-parameter
    """

    decoded = base64.urlsafe_b64decode(ei)

    # grab 1st 4 bytes and treat as LE unsigned int
    timestamp = struct.unpack('<i', decoded[0:4])[0]
    parsed = [timestamp]

    varint_offset = 4  # First 4 (0-3) bytes are the timestamp
    for _ in [1, 2, 3]:
        value, bytes_used = decode_varint(decoded[varint_offset:])
        parsed.append(value)
        varint_offset += bytes_used

    return parsed


def parse_rlz(rlz_string):
    # Reference: https://github.com/rogerta/rlz/blob/wiki/HowToReadAnRlzString.md

    rlz = {}
    assert rlz_string[0] == '1', 'Only v1 of RLZ is known'

    rlz['version'] = {
            'data_type': 'google.rlz.version',
            'key': 'RLZ version',
            'value': rlz_string[0],
            'hover': 'Only v1 of RLZ is known'}

    rlz['ap'] = {
        'data_type': 'google.rlz.ap',
        'key': 'Application',
        'value': rlz_string[1:3],
        'hover': 'Application (or "access point") used to do the Google Search'}

    rlz['brand_code'] = {
        'data_type': 'google.rlz.brand_code',
        'key': 'Brand Code',
        'value': rlz_string[3:7],
        'hover': 'The brand code identifies the distribution channel (it may be a partner or internal marketing). <br>'
                 'This correlates to how the user got the software (ie. they downloaded it by itself vs. it came <br>'
                 'pre-installed on their new computer vs. it came with a partner\'s software.'}

    cannibal_string = rlz_string[7]
    if cannibal_string == 'c':
        cannibal_value = 'Yes'
    elif cannibal_string == '_':
        cannibal_value = 'No'
    else:
        raise ValueError(f'Invalid "cannibal" value in RLZ string: {cannibal_string}')

    rlz['cannibal'] = {
        'data_type': 'google.rlz.cannibal',
        'key': 'Cannibalized',
        'value': cannibal_value,
        'hover': '"Cannibal" tells if the library has evidence that the user was a user prior <br>'
                 'to installing the software, and thus "cannibalized" a previous installation.'}

    rlz_pointer = 8

    # Examples of longer RLZ values (2- and 5-char lang codes):
    #   1C1CHBF_en-GBGB901GB901
    #   1C1GCEU_enUS820US820
    if len(rlz_string) >= 11:
        # If a dash is in this position, it means it is a 5 char lang code, not the 2 char code
        if rlz_string[10] == '-':
            language_code = rlz_string[rlz_pointer:rlz_pointer+5]
            rlz_pointer += 5
            # langcodes was having install issues on macOS; not using it for now in
            # order to not complicate Unfurl's install. Pycountry's languages isn't
            # as good (only alpha_2 and alpha_3) but better than nothing for now.
            # Old implementation:
            # language_name = langcodes.Language.get(language_code).language_name()
            language_name = pycountry.languages.get(alpha_2=language_code[:2]).name

        else:
            language_code = rlz_string[rlz_pointer:rlz_pointer+2]
            # language_name = langcodes.Language.get(language_code).language_name()
            language_name = pycountry.languages.get(alpha_2=language_code).name
            rlz_pointer += 2

    # Example of RLZ value without cohorts
    #   1C1GCEV_en
    elif len(rlz_string) == 10:
        language_code = rlz_string[rlz_pointer:rlz_pointer + 2]
        # language_name = langcodes.Language.get(language_code).language_name()
        language_name = pycountry.languages.get(alpha_2=language_code).name
        rlz_pointer += 2

    else:
        raise ValueError('Couldn\'t parse RLZ language code')

    rlz['language'] = {
        'data_type': 'google.rlz.language',
        'key': 'Language',
        'value': f'{language_name} ({language_code})',
        'hover': 'The two- (en) or five-character (zh-CN) language code of the application. <br>'
                 'Valid values depend on the specific app.'}

    # The cohorts are optional, so if this is the end of the RLZ string, return what we've parsed
    if not len(rlz_string) >= rlz_pointer+5:
        return rlz

    install_cohort = rlz_string[rlz_pointer:rlz_pointer+5]
    rlz_pointer += 5

    install_country_code = install_cohort[:2]
    install_country = pycountry.countries.get(alpha_2=install_country_code).name
    install_date = datetime.timedelta(weeks=int(install_cohort[2:])) + datetime.date(year=2003, month=2, day=3)

    rlz['install_cohort'] = {
        'data_type': 'google.rlz.install_cohort',
        'key': 'Install Cohort',
        'value': f'Installed in {install_country} the week of {install_date}',
        'hover': 'The country and week of the user\'s installation event. <br>'
                 'Country is determined by the server, using IP address. <br>'
                 'Week is measured as number of weeks since Feb 3, 2003.'}

    # Both cohorts do not need to be present, so if the 2nd one (search) is missing, return what we have
    # Example: 1CAGZLV_enGB898
    if not len(rlz_string) >= rlz_pointer + 5:
        return rlz

    search_cohort = rlz_string[rlz_pointer:rlz_pointer + 5]

    search_country_code = search_cohort[:2]
    search_country = pycountry.countries.get(alpha_2=search_country_code).name
    search_date = datetime.timedelta(weeks=int(search_cohort[2:])) + datetime.date(year=2003, month=2, day=3)

    rlz['search_cohort'] = {
        'data_type': 'google.rlz.search_cohort',
        'key': 'Search Cohort',
        'value': f'First search was in {search_country} the week of {search_date}',
        'hover': 'The country and week of the user\'s first search. <br>'
                 'Country is determined by the server, using IP address. <br>'
                 'Week is measured as number of weeks since Feb 3, 2003.'}

    return rlz


def run(unfurl, node):
    if node.data_type == 'url.query.pair':
        if 'google' in unfurl.find_preceding_domain(node):
            if node.key == 'bih':
                unfurl.add_to_queue(
                    data_type='google.bih', key='Browser Height', value=node.value,
                    label=f'Browser height: {node.value}px',
                    hover='Inner height of the browser window',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'biw':
                unfurl.add_to_queue(
                    data_type='google.biw', key='Browser Width', value=node.value,
                    label=f'Browser width: {node.value}px',
                    hover='Inner width of the browser window',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'ei':
                parsed_ei = parse_ei(unfurl.add_b64_padding(node.value))
                node.hover = 'The \'<b>ei</b>\' parameter is base64-encoded and contains four values. ' \
                             '<br>The first two are thought to be the timestamp of when the session started ' \
                             '<br>(first value is full seconds, second is microsecond component)' \
                             '<br>This may be seconds (but could be days!) before the URL was generated.' \
                             '<br><br>References:<ul>' \
                             '<li><a href="https://deedpolloffice.com/blog/articles/decoding-ei-parameter" ' \
                             'target="_blank">Kevin Jones: How to decode the ei parameter in Google search</a></li>' \
                             '<li><a href="http://cheeky4n6monkey.blogspot.com/2014/10/google-eid.html" ' \
                             'target="_blank">Cheeky4n6Monkey: Google-ei\'d ?!</a></li>' \
                             '<li><a href="https://github.com/obsidianforensics/unfurl/issues/56" ' \
                             'target="_blank">Rasmus-Riis: Search Experiment with ei parameter</a></li>'\
                             '<li>Adam Mazack: noticed the 2nd ei value contained fractional seconds ' \
                             '<br> that match the ved</li></ul>'
                node.extra_options = {'widthConstraint': {'maximum': 300}}

                assert len(parsed_ei) == 4, \
                    f'There should be 4 decoded ei values, but we have {len(parsed_ei)}!'

                # The first ei value is epoch seconds, the second has the fractional (micro) seconds.
                # Concatenating them here as strings lets the timestamp parser convert it later.
                ei_timestamp = str(parsed_ei[0]) + str(parsed_ei[1])

                unfurl.add_to_queue(
                    data_type='epoch-microseconds', key=None, value=ei_timestamp, label=f'ei Timestamp: {ei_timestamp}',
                    hover='The first two values combined in the <b>ei</b> parameter are thought to be the timestamp of '
                          'when the session began.', parent_id=node.node_id, incoming_edge_config=google_edge)

                unfurl.add_to_queue(
                    data_type='integer', key=None, value=parsed_ei[2],
                    label=f'ei-2: {parsed_ei[2]}',
                    hover='The meaning of the third <b>ei</b> value is not known.',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

                unfurl.add_to_queue(
                    data_type='integer', key=None, value=parsed_ei[3],
                    label=f'ei-3: {parsed_ei[3]}',
                    hover='The meaning of the fourth <b>ei</b> value is not known, '
                          'but it matches the <b>ved</b> "13-3" value.',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'gs_l':
                node.hover = 'The <b>gs_l</b> parameter contains multiple values, delimited by <b>.</b>. <br>' \
                             'We only know the meaning of 7 (of the 26+) parameters.'
                node.extra_options = {'widthConstraint': {'maximum': 1400}}

                params = node.value.split('.')

                known_params = [0, 1, 2, 4, 5, 7, 8, 26]
                for known_param in known_params:
                    if len(params[known_param]) > 0:
                        unfurl.add_to_queue(
                            data_type='google.gs_l', key=str(known_param), value=params[known_param],
                            label=f'Parameter {str(known_param)}: {params[known_param]}',
                            parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'oq':
                unfurl.add_to_queue(
                    data_type='google.oq', key=None, value=f'"Original" Search Query: {node.value}',
                    hover='Original terms entered by the user; auto-complete or suggestions <br>'
                          'may have been used to reach the actual search terms (in <b>q</b>)',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'q':
                unfurl.add_to_queue(
                    data_type='google.q', key=None, value=f'Search Query: {node.value}',
                    hover='Terms used in the Google search', parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'source':
                if node.value in known_sources.keys():
                    unfurl.add_to_queue(
                        data_type='google.source', key=None, value=f'Source: {known_sources[node.value]}',
                        hover='Source of the Google search', parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'start':
                unfurl.add_to_queue(
                    data_type='google.start', key=None, value=f'Starting Result: {node.value}',
                    hover='Google search by default shows 10 results per page; higher <br>'
                          '"start" values may indicate browsing more subsequent results pages.',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'sxsrf':
                node.extra_options = {'widthConstraint': {'maximum': 400}}
                sxs_0, sxs_1 = node.value.split(':', 1)
                unfurl.add_to_queue(data_type='google.sxsrf', key=1, value=sxs_0,
                                    parent_id=node.node_id, incoming_edge_config=google_edge)
                unfurl.add_to_queue(
                    data_type='epoch-milliseconds', key=2, value=sxs_1,
                    hover='The <b>sxsrf</b> parameter contains a timestamp, believed<br>'
                          ' to correspond to the previous page load. <br><br>Refernces:<ul><li>'
                          '<a href="https://twitter.com/phillmoore/status/1169846359509233664" target="_blank">'
                          'Phill Moore on Twitter</a></li></ul>', parent_id=node.node_id,
                    incoming_edge_config=google_edge)

            elif node.key == 'tbm':
                tbm_mappings = {
                    'bks': 'Google Books',
                    'fin': 'Google Finance',
                    'flm': 'Google Flights',
                    'isch': 'Google Images',
                    'nws': 'Google News',
                    'shop': 'Google Shopping',
                    'vid': 'Google Videos',
                }

                value = tbm_mappings.get(node.value, 'Unknown')
                unfurl.add_to_queue(
                    data_type='google.tbm', key=None, value=f'Search Type: {value}',
                    hover='Google Search Type', parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'uule':
                # https://moz.com/ugc/geolocation-the-ultimate-tip-to-emulate-local-search
                location_string = base64.b64decode(unfurl.add_b64_padding(node.value[10:]))
                unfurl.add_to_queue(
                    data_type='google.uule', key=None, value=location_string, label=location_string,
                    parent_id=node.node_id, incoming_edge_config=google_edge)

            elif node.key == 'rlz':
                unfurl.add_to_queue(
                    data_type='descriptor', key=None,
                    value='RLZ used for grouping promotion event signals and anonymous user cohorts',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

                try:
                    rlz = parse_rlz(node.value)

                    for component in rlz.values():
                        unfurl.add_to_queue(
                            data_type=component['data_type'], key=component['key'],
                            value=component['value'], hover=component['hover'],
                            parent_id=node.node_id, incoming_edge_config=google_edge)

                except ValueError as e:
                    print(f'Exception parsing RLZ: {e}')

            elif node.key == 'ved':
                node.extra_options = {'widthConstraint': {'maximum': 400}}
                known_ved_descriptions = {
                    'linkIndex':
                        'Unique index for each link on the search page. <br>The higher the number, the farther'
                        ' down the page the link is. <br>This should always be present. '
                        '<a href="https://deedpolloffice.com/blog/articles/decoding-ved-parameter" '
                        'target="_blank">[ref]</a>',
                    'linkType':
                        'The type of link that was clicked on; there are thousands. <br>This should always be '
                        'present. <a href="https://deedpolloffice.com/blog/articles/decoding-ved-parameter" '
                        'target="_blank">[ref]</a>',
                    'subResultPosition':
                        'The position of the link, if it was inside a "group" (like an adword or<br> '
                        'knowledge graph). This starts at 0 and counts up.'
                        '<a href="https://deedpolloffice.com/blog/articles/decoding-ved-parameter" '
                        'target="_blank">[ref]</a>',
                    'resultPosition':
                        'The position of the result on the page. The higher the number, <br>the farther '
                        'down the page the result is. '
                        '<a href="https://deedpolloffice.com/blog/articles/decoding-ved-parameter" '
                        'target="_blank">[ref]</a>',
                    'resultsStart':
                        'The starting position of the first result on the page. <br>On page 2, it will be '
                        '10; and on page 3 it will be 20, <br>and so on. On page 1, the value isn’t '
                        'present (but implicitly, this means a value of 0).'
                        '<a href="https://deedpolloffice.com/blog/articles/decoding-ved-parameter" '
                        'target="_blank">[ref]</a>',
                }
                assert node.value[0] in ['0', '2'], 'The ved parameter should start with 0 or 2'
                encoded_ved = node.value[1:]
                encoded_ved = base64.urlsafe_b64decode(unfurl.add_b64_padding(encoded_ved))
                ved = Ved().FromString(encoded_ved)
                ved_dict = json_format.MessageToDict(ved)
                for key, value in ved_dict.items():
                    if key == 'v13Outer':
                        assert isinstance(value, dict), 'ved-13-Outer should be a dict'
                        assert isinstance(value['v13Inner'], dict), 'ved-13-Inner should also be a dict'
                        v13_timestamp = value['v13Inner'].get('timestamp')
                        if v13_timestamp:
                            unfurl.add_to_queue(
                                data_type='epoch-microseconds', key='Timestamp', value=v13_timestamp,
                                parent_id=node.node_id, incoming_edge_config=google_edge,
                                hover='The ved parameter contains a timestamp, believed to <br>correspond to around '
                                      'when the page loaded.')

                        v13_unknown_2 = value['v13Inner'].get('v132')
                        if v13_unknown_2:
                            unfurl.add_to_queue(
                                data_type='google.ved', key='13-2', value=v13_unknown_2,
                                parent_id=node.node_id, incoming_edge_config=google_edge,
                                hover='Inside the ved parameter, the meanings of<br> 13-2 and 13-3 are not known.')

                        v13_unknown_3 = value['v13Inner'].get('v133')
                        if v13_unknown_3:
                            unfurl.add_to_queue(
                                data_type='google.ved', key='13-3', value=v13_unknown_3,
                                parent_id=node.node_id, incoming_edge_config=google_edge,
                                hover='Inside the ved parameter, the meanings of 13-2 and 13-3 are not known, <br>'
                                      'but the values in <b>ved 13-3</b> and <b>ei-3</b> match.')

                    elif key == 'v15':
                        assert isinstance(value, dict), 'ved-15 should be a dict'
                        v15_1 = value.get('v151')
                        v15_2 = value.get('v152')

                        if v15_1:
                            unfurl.add_to_queue(
                                data_type='google.ved', key='15-1', value=v15_1,
                                parent_id=node.node_id, incoming_edge_config=google_edge,
                                hover='Inside the ved parameter, the meanings of<br> 15-1 and 15-2 are not known.')
                        if v15_2:
                            unfurl.add_to_queue(
                                data_type='google.ved', key='15-2', value=v15_2,
                                parent_id=node.node_id, incoming_edge_config=google_edge,
                                hover='Inside the ved parameter, the meanings of<br> 15-1 and 15-2 are not known.')

                    else:
                        unfurl.add_to_queue(
                            data_type='google.ved', key=key, value=value, label=f'{key}: {value}',
                            hover=known_ved_descriptions.get(key, ''),
                            parent_id=node.node_id, incoming_edge_config=google_edge)

    if node.data_type == 'google.gs_l':
        known_values = {
            '0': known_sources,
            '1': {
                '1': 'mouse-click on suggestion',
                '3': 'keyboard [enter] key',
                '10': 'Google Instant Search (untested)'
            }
        }
        if node.key == '0':
            if node.value in known_values[node.key].keys():
                unfurl.add_to_queue(
                    data_type='descriptor', key=None, value=known_values[node.key][node.value],
                    label=f'Searcher came from {known_values[node.key][node.value]}',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

        if node.key == '1':
            if node.value in known_values[node.key].keys():
                unfurl.add_to_queue(
                    data_type='descriptor', key=None, value=known_values[node.key][node.value],
                    label=f'Searcher selected search terms by {known_values[node.key][node.value]}',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

        if node.key == '2':
            unfurl.add_to_queue(
                data_type='descriptor', key=None, value=node.value,
                label=f'Selected option {node.value} from suggestion list',
                parent_id=node.node_id, incoming_edge_config=google_edge)

        if node.key == '4':
            if node.value == '0':
                param_text = 'User clicked on a suggestion'
            else:
                param_text = f'{str(float(node.value) / 1000)} seconds before the user selected the search box'

            unfurl.add_to_queue(
                data_type='descriptor', key=None, value=node.value, label=param_text,
                parent_id=node.node_id, incoming_edge_config=google_edge)

        if node.key == '5':
            if node.value == '0':
                param_text = 'User clicked on a suggestion'
            else:
                param_text = f'{str(float(node.value) / 1000)} seconds on page before the user completed typing.'

            unfurl.add_to_queue(
                data_type='descriptor', key=None, value=node.value, label=param_text,
                parent_id=node.node_id, incoming_edge_config=google_edge)

        if node.key == '7':
            if node.value != '0':
                param_text = f'User spent {str(float(node.value) / 1000)} seconds on page in total.'
                unfurl.add_to_queue(
                    data_type='descriptor', key=None, value=node.value, label=param_text,
                    parent_id=node.node_id, incoming_edge_config=google_edge)

        if node.key == '8':
            if node.value == '0':
                param_text = 'No characters typed'
            else:
                param_text = f'{node.value} keys pressed while user was typing.'

            unfurl.add_to_queue(
                data_type='descriptor', key=None, value=node.value, label=param_text,
                hover='If the search was done in Chrome, this value may be +1.',
                parent_id=node.node_id, incoming_edge_config=google_edge)

        if node.key == '26':
            if node.value == '1':
                unfurl.add_to_queue(
                    data_type='descriptor', key=None, value=node.value, label='User typed in query',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

    elif node.data_type == 'google.ved':
        known_link_types = {
            22: 'web',
            152: 'blog search result',
            232: 'book or patent search result',
            235: 'book or patent search result thumbnail',
            244: 'image result in standard SERPs',
            245: 'image search result in basic (non-javascript) image search, or image result in universal search',
            288: 'local search result',
            295: 'news result thumbnail',
            297: 'news result',
            300: 'more results link (listed mainly for Q&A websites)',
            311: 'video result',
            312: 'video result thumbnail',
            338: 'one-line sitelink',
            371: 'shopping search result',
            429: 'image search result [probably not in use any more]',
            586: '"Jump to" link',
            612: 'map search result website link',
            646: 'map search result thumbnail',
            706: 'adword sitelink',
            745: 'breadcrumb',
            1107: 'patent result "Overview" / "Related" / "Discuss" link',
            1140: 'book search result author link',
            1146: 'normal result thumbnail (e.g. for an application, recipe, etc.)',
            1150: 'normal result thumbnail (e.g. for an application, recipe, etc.)',
            1455: 'local search result marker pin icon',
            1532: 'news sub-result (i.e. the same story from a different site)',
            1617: 'adword (i.e. sponsored search result)',
            1701: 'map search result',
            1732: 'knowledge graph repeated sub-link (e.g. football team squad players, album track listings)',
            1907: 'sponsored shopping result thumbnail (in right-hand column of universal search results)',
            1908: 'sponsored shopping result (in right-hand column of universal search results)',
            1986: 'sponsored shopping result thumbnail (in main column of universal search results)',
            1987: 'sponsored shopping result (in main column of universal search results)',
            2060: 'sitelink',
            2237: 'news result video thumbnail',
            2459: 'knowledge graph link',
            2847: 'authorship "by [author]" link',
            2937: 'authorship thumbnail link',
            3588: 'image search result (thumbnail)',
            3596: 'image search result preview "View image" link',
            3597: 'image search result preview thumbnail',
            3598: 'image search result preview title link',
            3599: 'image search result preview "Visit page" link',
            3724: 'image search result preview grey website link underneath title',
            3836: 'knowledge graph main image',
            5077: 'in-depth article result',
            5078: 'in-depth article result thumbnail',
            5158: 'adword one-line sitelink',
            5497: 'dictionary definition link'
        }

        if node.key == 'linkType':
            if known_link_types.get(node.value):
                unfurl.add_to_queue(
                    data_type='descriptor', key=None, value=node.value, label=known_link_types.get(node.value),
                    hover='There are tens of thousands of these values; the \'known\'<br> ones in Unfurl are based on '
                          '<a href="https://github.com/beschulz/ved-decoder" target="_blank">'
                          'Benjamin Schulz\'s work</a>',
                    parent_id=node.node_id, incoming_edge_config=google_edge)

    elif node.data_type == 'google.rlz.ap':
        # From https://source.chromium.org/chromium/chromium/src/+/master:rlz/lib/lib_values.cc
        rlz_aps = {
            # 'I7': 'IE_DEFAULT_SEARCH',
            'I7': 'IE Default search',
            # 'W1': 'IE_HOME_PAGE',
            'W1': 'IE Home Page',
            # 'T4': 'IETB_SEARCH_BOX',
            'T4': 'IE Toolbar Search Box',
            'Q1': 'QUICK_SEARCqH_BOX',
            'D1': 'GD_DESKBAND',
            'D2': 'GD_SEARCH_GADGET',
            'D3': 'GD_WEB_SERVER',
            'D4': 'GD_OUTLOOK',
            # 'C1': 'CHROME_OMNIBOX',
            'C1': 'Chrome Omnibox',
            # 'C2': 'CHROME_HOME_PAGE',
            'C2': 'Chrome Home Page',
            # 'B2': 'FFTB2_BOX',
            'B2': 'Firefox Toolbar v2',
            # 'B3': 'FFTB3_BOX',
            'B3': 'Firefox Toolbar v3',
            'N1': 'PINYIN_IME_BHO',
            'G1': 'IGOOGLE_WEBPAGE',
            'H1': 'MOBILE_IDLE_SCREEN_BLACKBERRY',
            'H2': 'MOBILE_IDLE_SCREEN_WINMOB',
            'H3': 'MOBILE_IDLE_SCREEN_SYMBIAN',
            # 'R0': 'FF_HOME_PAGE',
            'R0': 'Firefox Home Page',
            # 'R1': 'FF_SEARCH_BOX',
            'R1': 'Firefox Search box',
            'R2': 'IE_BROWSED_PAGE',
            'R3': 'QSB_WIN_BOX',
            'R4': 'WEBAPPS_CALENDAR',
            'R5': 'WEBAPPS_DOCS',
            'R6': 'WEBAPPS_GMAIL',
            'R7': 'IETB_LINKDOCTOR',
            'R8': 'FFTB_LINKDOCTOR',
            'T7': 'IETB7_SEARCH_BOX',
            'T8': 'TB8_SEARCH_BOX',
            'C3': 'CHROME_FRAME',
            'V1': 'PARTNER_AP_1',
            'V2': 'PARTNER_AP_2',
            'V3': 'PARTNER_AP_3',
            'V4': 'PARTNER_AP_4',
            'V5': 'PARTNER_AP_5',
            # 'C5': 'CHROME_MAC_OMNIBOX',
            'C5': 'Chrome Omnibox on Mac',
            # 'C6': 'CHROME_MAC_HOME_PAGE',
            'C6': 'Chrome home page on Mac',
            # 'CA': 'CHROMEOS_OMNIBOX',
            'CA': 'ChromeOS Omnibox',
            # 'CB': 'CHROMEOS_HOME_PAGE',
            'CB': 'ChromeOS Home Page',
            'CC': 'CHROMEOS_APP_LIST',
            # 'C9': 'CHROME_IOS_OMNIBOX_TABLET',
            'C9': 'Chrome Omnibox on iOS Tablet',
            # 'CD': 'CHROME_IOS_OMNIBOX_MOBILE',
            'CD': 'Chrome Omnibox on iOS Mobile',
            'C7': 'CHROME_APP_LIST',
            'C8': 'CHROME_MAC_APP_LIST',
            'RQ': 'UNDEFINED_AP_Q',
            'RR': 'UNDEFINED_AP_R',
            'RS': 'UNDEFINED_AP_S',
            'RT': 'UNDEFINED_AP_T',
            'RU': 'UNDEFINED_AP_U',
            'RV': 'UNDEFINED_AP_V',
            'RW': 'UNDEFINED_AP_W',
            'RX': 'UNDEFINED_AP_X',
            'RY': 'UNDEFINED_AP_Y',
            'RZ': 'UNDEFINED_AP_Z',
            'U0': 'PACK_AP0',
            'U1': 'PACK_AP1',
            'U2': 'PACK_AP2',
            'U3': 'PACK_AP3',
            'U4': 'PACK_AP4',
            'U5': 'PACK_AP5',
            'U6': 'PACK_AP6',
            'U7': 'PACK_AP7',
            'U8': 'PACK_AP8',
            'U9': 'PACK_AP9',
            'UA': 'PACK_AP10',
            'UB': 'PACK_AP11',
            'UC': 'PACK_AP12',
            'UD': 'PACK_AP13'
        }

        unfurl.add_to_queue(
            data_type='descriptor', key=node.value, value=rlz_aps.get(node.value, 'Unknown'),
            label=f'Search performed using {rlz_aps.get(node.value, "unknown application")}',
            parent_id=node.node_id, incoming_edge_config=google_edge)
