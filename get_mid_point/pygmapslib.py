#!/usr/bin/env python
#coding: UTF-8
#
# Kensuke Narita - 2014
# Based on pygeocoder by Xiao Yu, Se'bastien Fievet and Marius Grigaitis.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Python wrapper for Google Maps API V3.

"""

import traceback
import requests
import base64
import hmac
import hashlib
from __version__ import VERSION

try:
    import json
except ImportError:
    import simplejson as json

__all__ = ['PyGMapsError', 'PyGMaps']

class PyGMapsError(Exception):
    def __init__(self, http_status_code, url):
        self.http_status_code = http_status_code
        self.url = url

    def __str__(self):
        return 'HTTTP STATUS CODE:%d\nURL:%s' % (self.http_status_code, self.url)

    def __unicode__(self):
        return unicode(self.__str__())

class PyGMaps(object):
    def __init__(self, client_id=None, private_key=None):
        self.client_id = client_id
        self.private_key = private_key
        self.proxy = None

    def set_proxy(self, proxy):
        self.proxy = proxy

    def add_signature(self, request):
        decoded_key = base64.urlsafe_b64decode(str(self.private_key))
        signature = hmac.new(decoded_key, request.url, hashlib.sha1)
        encoded_signature = base64.urlsafe_b64encode(signature.digest())
        request.params['client'] = str(self.client_id)
        request.params['signature'] = encoded_signature

    def get_data(self, query_url, params):
#メモ
#http://docs.python-requests.org/en/latest/api/#requests.PreparedRequest
        request = requests.Request('GET',
                url = query_url,
                params = params,
                headers = {
                    'User-Agent': 'PyGMaps/' + VERSION + ' (Python)'
                })

        if self.client_id and self.private_key:
            self.add_signature(request)

        session = requests.Session()

        if self.proxy:
            session.proxies = {'https': self.proxy}

        response = session.send(request.prepare())
        session.close()

        if response.status_code != 200:
            raise PyGMapsError(response.status_code, response.url)

        return response.json()

