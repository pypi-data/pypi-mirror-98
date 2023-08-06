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
Package "selfservice.template"
"""
API_VERSION = "1.10.0"

from delphixpy.v1_10_0 import response_validator

def create(engine, js_data_template_create_parameters):
    """
    Create a new JSDataTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_10_0.delphix_engine.DelphixEngine`
    :param js_data_template_create_parameters: Payload object.
    :type js_data_template_create_parameters:
        :py:class:`v1_10_0.web.vo.JSDataTemplateCreateParameters`
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/selfservice/template"
    response = engine.post(url, js_data_template_create_parameters.to_dict(dirty=True) if js_data_template_create_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified JSDataTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_10_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_10_0.web.objects.JSDataTemplate.JSDataTemplate`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_10_0.web.vo.JSDataTemplate`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/selfservice/template/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSDataTemplate'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    List the data templates defined in the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_10_0.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_10_0.web.vo.JSDataTemplate`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/selfservice/template"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSDataTemplate'], returns_list=True, raw_result=raw_result)

def update(engine, ref, js_data_template=None):
    """
    Update the specified JSDataTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_10_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_10_0.web.objects.JSDataTemplate.JSDataTemplate`
        object
    :type ref: ``str``
    :param js_data_template: Payload object.
    :type js_data_template: :py:class:`v1_10_0.web.vo.JSDataTemplate`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/selfservice/template/%s" % ref
    response = engine.post(url, js_data_template.to_dict(dirty=True) if js_data_template else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified JSDataTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_10_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_10_0.web.objects.JSDataTemplate.JSDataTemplate`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/selfservice/template/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def get_num_containers(engine, ref):
    """
    Returns the number of non-replicated Self-Service data containers forked
    from this template.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_10_0.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_10_0.web.objects.JSDataTemplate.JSDataTemplate`
        object
    :type ref: ``str``
    :rtype: ``int``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/selfservice/template/%s/getNumContainers" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['int'], returns_list=False, raw_result=raw_result)

