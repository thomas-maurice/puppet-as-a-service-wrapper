#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
         DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                Version 2, December 2004
 Copyright (C) 2015 Thomas Maurice <thomas@maurice.fr>
 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
  0. You just DO WHAT THE FUCK YOU WANT TO.
"""

import ConfigParser
import requests
import os

from requests.compat import urljoin


class APIError(Exception):
    """Base exception class"""


class InvalidResponse(APIError):
    """Raised when api response is not valid json"""


class ResourceNotFoundError(APIError):
    """Raised when requested resource does not exist."""


class BadParametersError(APIError):
    """Raised when request contains bad parameters."""


class NetworkError(APIError):
    """Raised when there is an error from network layer."""


class Forbidden(APIError):
    """Raised when there is a permission issue"""


class ConfigurationNotFoundException(APIError):
    """Raised when there is an error from network layer."""


class ApiClient():
    def __init__(self):
        """We try to load the conf from  a set of defined pathes"""
        conf_file = None
        for path in [
            "ppaas.conf",
            os.path.join(os.environ.get('HOME', ""), ".ppaas.conf"),
            "/etc/ppaas.conf"
        ]:
            if os.path.exists(path):
                conf_file = path
                break
        if conf_file is None:
            raise ConfigurationNotFoundException
        conf = ConfigParser.ConfigParser()
        conf.read(conf_file)
        self.user = conf.get('auth', 'user')
        self.passw = conf.get('auth', 'pass')
        self.endpoint = conf.get('api', 'endpoint')
        self.timeout = 10

    def get(self, url, params=None):
        return self.call('GET', urljoin(self.endpoint, url), params=params)

    def post(self, url, data=None, params=None):
        return self.call('POST', urljoin(self.endpoint, url), data=data)

    def put(self, url, data, params=None):
        return self.call('PUT', urljoin(self.endpoint, url), data=data, params=params)

    def delete(self, url, params=None):
        return self.call('DELETE', urljoin(self.endpoint, url), params=params)

    def call(self, method, path, data=None, params=None):
        body = ''

        call_result = requests.request(
            method,
            path,
            params=params,
            auth=(self.user, self.passw),
            json=body,
            timeout=self.timeout
        )
        status = call_result.status_code
        result = None

        try:
            if call_result.text:
                result = call_result.json()
        except ValueError as error:
            raise InvalidResponse("Failed to decode API response", error)

        if status >= 100 and status < 300:
            return result, status
        elif status == 403:
            raise Forbidden(result)
        elif status == 404:
            raise ResourceNotFoundError(result)
        elif status == 400:
            raise BadParametersError(result)
        elif status == 0:
            raise NetworkError()
        else:
            raise APIError("%d: %s" % (status, result))
