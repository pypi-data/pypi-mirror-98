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
Package "timezone"
"""
API_VERSION = "1.8.2"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_8_2 import response_validator

def get_all(engine, date=None):
    """
    Lists all of the supported time zones.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_8_2.delphix_engine.DelphixEngine`
    :param date: The offset of this time zone from UTC is calculated at this
        date. If Daylight Saving Time is in effect at the specified date, the
        offset value is adjusted with the amount of daylight saving. If no date
        is specified then a default time of now is used.
    :type date: ``TEXT_TYPE``
    :rtype: ``list`` of :py:class:`v1_8_2.web.vo.TimeZone`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/timezone"
    query_params = {"date": date}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TimeZone'], returns_list=True, raw_result=raw_result)

