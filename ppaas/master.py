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
from certificate import Certificate


def pretty_print(d):
    return json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))


class Master(object):
    def __init__(self, uuid):
        self.client = ApiClient()
        self.uuid = uuid
        self.cached_data, _ = self.client.get('/masters/%s' % self.uuid)

    @staticmethod
    def get_masters(client=None):
        if not client:
            client = ApiClient()
        result, status = client.get('/masters')
        masters = []
        for master in result['masters']:
            masters.append(Master(master['id']))
        return masters

    @staticmethod
    def get_master(name, client=None):
        if not client:
            client = ApiClient()
        masters = Master.get_masters(client)
        for master in masters:
            if master.cached_data['name'] == name:
                return master
        return None

    def get_certificates(self, status=None):
        if status is None:
            return Certificate.get_certificates(self, self.client)
        else:
            certificates = Certificate.get_certificates(self, self.client)
            return [cert for cert in certificates if cert.status['message'] == status]

    def __repr__(self):
        return "<Puppet Master %s>" % self.uuid

    def refresh(self):
        try:
            self.client.post('/masters/%s/refresh' % self.uuid)
            return True
        except:
            return False

    def restart(self):
        try:
            self.client.post('/masters/%s/restart' % self.uuid)
            return True
        except:
            return False

    def certificate(self, hostname):
        return Certificate(self, hostname)

    @property
    def crl(self):
        data, result = self.client.get('/masters/%s/crl' % self.uuid)
        return data['crl']

    @property
    def certificates(self):
        data, result = self.client.get('/masters/%s/certs' % self.uuid)
        return data['certs']

    @property
    def environments(self):
        data, result = self.client.get('/masters/%s/environments' % self.uuid)
        return data['environments']

    @property
    def last_update(self):
        data, result = self.client.get('/masters/%s/last-update' % self.uuid)
        return data['result']

    def to_dict(self):
        result, status = self.client.get('/masters')
        return result

    def __getattr__(self, name):
        data, status = self.client.get('/masters/%s' % self.uuid)
        if name in data:
            return data[name]
        return super(Master, self).__getattr__(name)
