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
Package "job"
"""
API_VERSION = "1.4.1"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_4_1 import response_validator

def get(engine, ref):
    """
    Retrieve the specified Job object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_4_1.web.objects.Job.Job`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_4_1.web.vo.Job`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/job/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Job'], returns_list=False, raw_result=raw_result)

def get_all(engine, add_events=None, from_date=None, job_state=None, page_offset=None, page_size=None, target=None, to_date=None):
    """
    Returns a list of jobs in the system.  Jobs are listed in start time order.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param add_events: Whether to include the job events in each job.
    :type add_events: ``bool``
    :param from_date: Filters out jobs older than this date.
    :type from_date: ``TEXT_TYPE``
    :param job_state: Limit jobs to those in the specified job state.
        *(permitted values: INITIAL, RUNNING, SUSPENDED, CANCELED, COMPLETED,
        FAILED)*
    :type job_state: ``TEXT_TYPE``
    :param page_offset: Page offset within job list.
    :type page_offset: ``int``
    :param page_size: Limit the number of jobs returned.
    :type page_size: ``int``
    :param target: Limit jobs to those affecting a particular object on the
        system. The target is the object reference for the target in question.
    :type target: ``TEXT_TYPE``
    :param to_date: Filters out jobs newer than this date.
    :type to_date: ``TEXT_TYPE``
    :rtype: ``list`` of :py:class:`v1_4_1.web.vo.Job`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/job"
    query_params = {"addEvents": add_events, "fromDate": from_date, "jobState": job_state, "pageOffset": page_offset, "pageSize": page_size, "target": target, "toDate": to_date}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Job'], returns_list=True, raw_result=raw_result)

def update(engine, ref, job=None):
    """
    Update the specified Job object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_4_1.web.objects.Job.Job`
        object
    :type ref: ``str``
    :param job: Payload object.
    :type job: :py:class:`v1_4_1.web.vo.Job`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/job/%s" % ref
    response = engine.post(url, job.to_dict(dirty=True) if job else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def cancel(engine, ref):
    """
    Cancel the specified job.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_4_1.web.objects.Job.Job`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/job/%s/cancel" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def request_report(engine, ref):
    """
    Request report of operation.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_4_1.web.objects.Job.Job`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_4_1.web.vo.FileDownloadResult`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/job/%s/requestReport" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['FileDownloadResult'], returns_list=False, raw_result=raw_result)

def resume(engine, ref):
    """
    Resume the specified job.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_4_1.web.objects.Job.Job`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/job/%s/resume" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def suspend(engine, ref):
    """
    Suspend the specified job.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_4_1.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_4_1.web.objects.Job.Job`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/job/%s/suspend" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

