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
Package "storage.test"
"""
API_VERSION = "1.8.0"

from delphixpy.v1_8_0 import response_validator

def create(engine, storage_test_parameters=None):
    """
    Create a new StorageTest object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_8_0.delphix_engine.DelphixEngine`
    :param storage_test_parameters: Payload object.
    :type storage_test_parameters:
        :py:class:`v1_8_0.web.vo.StorageTestParameters`
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/test"
    response = engine.post(url, storage_test_parameters.to_dict(dirty=True) if storage_test_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified StorageTest object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_8_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_8_0.web.objects.StorageTest.StorageTest` object
    :type ref: ``str``
    :rtype: :py:class:`v1_8_0.web.vo.StorageTest`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/test/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['StorageTest'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    Returns the list of previously executed tests.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_8_0.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_8_0.web.vo.StorageTest`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/test"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['StorageTest'], returns_list=True, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified StorageTest object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_8_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_8_0.web.objects.StorageTest.StorageTest` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/test/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def result(engine, ref):
    """
    Retrieve the text result of the storage test.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_8_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_8_0.web.objects.StorageTest.StorageTest` object
    :type ref: ``str``
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/test/%s/result" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

