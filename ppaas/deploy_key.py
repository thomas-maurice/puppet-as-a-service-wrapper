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


from api_client import ApiClient


class DeployKey(object):
    def __init__(self, name):
        self.client = ApiClient()
        self.name = name
        self.cached_data, _ = self.client.get('/deploy-keys/%s' % (self.name))

    @staticmethod
    def get_deploy_keys(client=None):
        if not client:
            client = ApiClient()
        result, status = client.get('/deploy-keys')
        keys = []
        for key in result['deploy_keys']:
            keys.append(DeployKey(key['name']))
        return keys

    @staticmethod
    def create_deploy_key(name, client=None):
        if not client:
            client = ApiClient()
        result, status = client.post('/deploy-keys', data={'name': name})
        return DeployKey(name)

    def delete(self):
        result, status = self.client.delete('/deploy-keys/%s' % (self.name))
        return result

    def __repr__(self):
        return "<Deploy Key %s>" % (self.name)

    def __getattr__(self, name):
        data, status = self.client.get('/deploy-keys/%s' % (self.name))
        if name in data:
            return data[name]
        return super(DeployKey, self).__getattr__(name)
