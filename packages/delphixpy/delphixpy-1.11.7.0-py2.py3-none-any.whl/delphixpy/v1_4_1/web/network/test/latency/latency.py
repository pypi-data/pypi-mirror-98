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
Package "network.test.latency"
"""
API_VERSION = "1.4.1"

from delphixpy.v1_4_1 import response_validator

def create(engine, network_latency_test_execute_parameters):
    """
    Create a new NetworkLatencyTest object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param network_latency_test_execute_parameters: Payload object.
    :type network_latency_test_execute_parameters:
        :py:class:`v1_4_1.web.vo.NetworkLatencyTestExecuteParameters`
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/network/test/latency"
    response = engine.post(url, network_latency_test_execute_parameters.to_dict(dirty=True) if network_latency_test_execute_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified NetworkLatencyTest object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_4_1.web.objects.NetworkL
        atencyTest.NetworkLatencyTest` object
    :type ref: ``str``
    :rtype: :py:class:`v1_4_1.web.vo.NetworkLatencyTest`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/network/test/latency/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['NetworkLatencyTest'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    Returns the list of previously executed tests.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_4_1.web.vo.NetworkLatencyTest`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/network/test/latency"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['NetworkLatencyTest'], returns_list=True, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified NetworkLatencyTest object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_4_1.web.objects.NetworkL
        atencyTest.NetworkLatencyTest` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/network/test/latency/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

