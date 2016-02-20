#!/usr/bin/env python

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

import json
import sys
import os

from api_client import ApiClient

class Certificate(object):
    def __init__(self, master, hostname):
        self.client = ApiClient()
        self.hostname = hostname
        self.master = master
        self.cached_data, _ = self.client.get('/masters/%s/certs/%s' % (self.master.uuid, hostname))

    @staticmethod
    def get_certificates(master, client=None):
        if not client:
            client = ApiClient()
        result, status = client.get('/masters/%s/certs' % master.uuid)
        certificates = []
        for certificate in result['certs']:
            certificates.append(Certificate(master, certificate['hostname']))
        return certificates

    def to_dict(self):
        result, status = self.client.get('/masters/%s/certs/%s' % (self.master.uuid, self.hostname))
        return result

    def __repr__(self):
        return "<Agent Certificate %s@%s>" % (self.hostname, self.master.uuid)

    def __getattr__(self, name):
        data, status = self.client.get('/masters/%s/certs/%s' % (self.master.uuid, self.hostname))
        if name in data:
            return data[name]
        return super(Certificate, self).__getattr__(name)
