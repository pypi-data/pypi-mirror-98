# coding: utf8
#
# Copyright 2021 by Delphix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Package "selfservice.usage.bookmark"
"""
API_VERSION = "1.11.7"

from delphixpy.v1_11_7.web.selfservice.usage.bookmark import tag
try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_11_7 import response_validator

def list_bookmark_usage_data(engine, data_layout=None):
    """
    Lists the usage breakdown for Self-Service bookmarks on a given data
    layout.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param data_layout: The usage information for the bookmarks on this data
        container will be returned.
    :type data_layout: ``TEXT_TYPE``
    :rtype: ``list`` of :py:class:`v1_11_7.web.vo.JSBookmarkUsageData`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/selfservice/usage/bookmark/listBookmarkUsageData"
    query_params = {"dataLayout": data_layout}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSBookmarkUsageData'], returns_list=True, raw_result=raw_result)

