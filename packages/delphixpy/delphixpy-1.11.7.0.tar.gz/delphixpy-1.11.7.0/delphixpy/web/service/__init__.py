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
Package "service"
"""
API_VERSION = "1.11.7"

from delphixpy.web.service import nfs
from delphixpy.web.service import httpConnector
from delphixpy.web.service import syslog
from delphixpy.web.service import linkingsettings
from delphixpy.web.service import smtp
from delphixpy.web.service import dns
from delphixpy.web.service import schema
from delphixpy.web.service import sso
from delphixpy.web.service import passwordVault
from delphixpy.web.service import kerberos
from delphixpy.web.service import support
from delphixpy.web.service import time
from delphixpy.web.service import userInterface
from delphixpy.web.service import tls
from delphixpy.web.service import minimalPhonehome
from delphixpy.web.service import phonehome
from delphixpy.web.service import proxy
from delphixpy.web.service import host
from delphixpy.web.service import locale
from delphixpy.web.service import insight
from delphixpy.web.service import cloud
from delphixpy.web.service import security
from delphixpy.web.service import userPaths
from delphixpy.web.service import ldap
from delphixpy.web.service import snmp
