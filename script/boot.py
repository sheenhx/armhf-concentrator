#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import logging
import sys
from time import *
import datetime, string
import httplib
import os

mac = os.environ['MAC']
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.info( "BOOT: update Consul K/V Status" )
conn = httplib.HTTPConnection('consul:8500')
conn.request('PUT', "/v1/kv/status/all", 'RUNNING')
response = conn.getresponse()
print response.status, response.reason
conn.close()

conn = httplib.HTTPConnection('consul:8500')
conn.request('PUT', "/v1/kv/status/"+mac+"", 'ready')
response = conn.getresponse()
print response.status, response.reason
conn.close()

logging.info( "BOOT: update Consul K/V to interval: 0ms." )
conn = httplib.HTTPConnection('consul:8500')
conn.request('PUT', '/v1/kv/interval', '0')
response = conn.getresponse()
print response.status, response.reason
