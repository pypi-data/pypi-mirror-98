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
Package "action"
"""
API_VERSION = "1.4.0"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_4_0 import response_validator

def get(engine, ref):
    """
    Retrieve the specified Action object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_4_0.web.objects.Action.Action` object
    :type ref: ``str``
    :rtype: :py:class:`v1_4_0.web.vo.Action`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/action/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Action'], returns_list=False, raw_result=raw_result)

def get_all(engine, from_date=None, page_offset=None, page_size=None, parent_action=None, root_action_only=None, state=None, to_date=None, user=None):
    """
    Retrieve an historical log of actions.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_0.delphix_engine.DelphixEngine`
    :param from_date: Start date for the search. Only actions on or after this
        date are included.
    :type from_date: ``TEXT_TYPE``
    :param page_offset: Offset within event list, in units of pageSize chunks.
    :type page_offset: ``int``
    :param page_size: Limit the number of events returned.
    :type page_size: ``int``
    :param parent_action: Limit actions to those with this parent action.
    :type parent_action: ``TEXT_TYPE``
    :param root_action_only: Limit actions to those without a parent action.
    :type root_action_only: ``bool``
    :param state: Limit actions to those in the specified state. *(permitted
        values: EXECUTING, WAITING, COMPLETED, FAILED, CANCELED)*
    :type state: ``TEXT_TYPE``
    :param to_date: End date for the search. Only actions on or before this
        date are included.
    :type to_date: ``TEXT_TYPE``
    :param user: Limit actions to those initiated by this user.
    :type user: ``TEXT_TYPE``
    :rtype: ``list`` of :py:class:`v1_4_0.web.vo.Action`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/action"
    query_params = {"fromDate": from_date, "pageOffset": page_offset, "pageSize": page_size, "parentAction": parent_action, "rootActionOnly": root_action_only, "state": state, "toDate": to_date, "user": user}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Action'], returns_list=True, raw_result=raw_result)

def get_job(engine, ref):
    """
    Get the job that is associated with this action.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_4_0.web.objects.Action.Action` object
    :type ref: ``str``
    :rtype: :py:class:`v1_4_0.web.vo.Job`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/action/%s/getJob" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Job'], returns_list=False, raw_result=raw_result)

