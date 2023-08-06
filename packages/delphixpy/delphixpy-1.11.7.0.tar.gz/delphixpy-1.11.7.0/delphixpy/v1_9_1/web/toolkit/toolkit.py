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
Package "toolkit"
"""
API_VERSION = "1.9.1"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_9_1 import response_validator

def get(engine, ref):
    """
    Retrieve the specified Toolkit object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_9_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_9_1.web.objects.Toolkit.Toolkit` object
    :type ref: ``str``
    :rtype: :py:class:`v1_9_1.web.vo.Toolkit`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Toolkit'], returns_list=False, raw_result=raw_result)

def get_all(engine, source_environment=None):
    """
    Lists installed toolkits.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_9_1.delphix_engine.DelphixEngine`
    :param source_environment: Restricts list to include only toolkits that are
        valid for the given source environment.
    :type source_environment: ``TEXT_TYPE``
    :rtype: ``list`` of :py:class:`v1_9_1.web.vo.Toolkit`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit"
    query_params = {"sourceEnvironment": source_environment}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Toolkit'], returns_list=True, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified Toolkit object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_9_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_9_1.web.objects.Toolkit.Toolkit` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

