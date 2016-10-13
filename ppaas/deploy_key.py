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

from .client import ApiClient


class DeployKey(object):
    """Interface for the /deploy-keys endpoints.

    This class allows you to interract with your deployments keys.

    This class has the following behavior:
      * When loaded it will cache some data in self.cached_data (it will
        cache its json representation according to the API)
      * Everytime you want to get data from the object, like key.fingerprint,
        the cache will be used, so make sure to call reload_datas if updates has been done.
      * Dictionnary lookup is done via the __getattr__ overloaded method. It
        is a bit hacky but it does the job. For instance to get the public part
        of your key, you can type `key.public`, this will query the
        cached value in the object

    An example json representation of what this class may look like :
    .. code-block:: json
        {
            "created_at": "2015-12-07T13:28:28",
            "name": "github",
            "fingerprint": "69:2f:e1:29:82:10:66:fa:59:a7:1e:22:40:66:1a",
            "public": "ssh-rsa AAAAB3NzaC1yc2EAAAAD[...]XP1BmhOtTOw=="
        }
    """
    def __init__(self, name, cached_data):
        """Creates a new object representing an *existing* deploy key

        :param name: The name of the deploy key you want to load
        :type name: str
        :param cached_data: Cached data to instantiate the master
        :type cached_data: dict

        :Example:

        >>> ppaas.DeployKey('thomas')
        <Deploy Key thomas>
        >>> ppaas.DeployKey('thomas').fingerprint
        u'52:35:1c:6c:12:57:5f:64:48:3b:ef:89:4c:c5:08:f9'
        >>> ppaas.DeployKey('Idontexist').fingerprint
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "ppaas/deploy_key.py", line 36, in __init__
            self.cached_data, _ = self.client.get('/deploy-keys/%s' % (self.name))
          File "ppaas/client.py", line 72, in get
            return self.call('GET', self.endpoint + url, params=params)
          File "ppaas/client.py", line 112, in call
            raise ResourceNotFoundError(result)
        ppaas.client.ResourceNotFoundError: {u'message': u'The requested resource could not be found.'}

        .. seealso:: get_deploy_keys(), create_deploy_key()
        """
        self.client = ApiClient()
        self.name = name
        self.reload_data(cached_data)

    def reload_data(self, refreshed_datas=None):
        """Reloads datas in the cached_data properties of a deploy key

        :param refreshed_datas: Data to use to reload cached_data property of deploy key
        :type refreshed_datas: dict

        """
        if refreshed_datas:
            self.cached_data = refreshed_datas
        else:
            self.cached_data, _ = self.client.get('/deploy-keys/%s' % (self.name))

    @staticmethod
    def get_deploy_keys(client=None):
        """Retrieves all your deployment keys.

        :param client: A client object you want to pass, if empty a new one will be created
        :type client: ApiClient

        :return: The list of your deployment keys
        :rtype: List of DeployKey objects

        :Example:

        >>> ppaas.DeployKey.get_deploy_keys()
        [<Deploy Key github>, <Deploy Key thomas>]
        """
        if not client:
            client = ApiClient()
        result, status = client.get('/deploy-keys')
        keys = []
        for key in result['deploy_keys']:
            keys.append(DeployKey(key['name'], key))
        return keys

    @staticmethod
    def create_deploy_key(name, client=None):
        """Creates a new deployment key with a given name.

        :param name: Name of the new key
        :type name: str

        :return: The newly created key
        :rtype: DeployKey

        :Example:

        >>> ppaas.DeployKey.create_deploy_key('fookey')
        <Deploy Key fookey>
        """
        if not client:
            client = ApiClient()
        result, status = client.post('/deploy-keys', data={'name': name})
        return DeployKey(name, result)

    def delete(self):
        """Deletes the current instance of DeployKey.

        :Exemple:

        >>> ppaas.DeployKey.get_deploy_keys()
        [<Deploy Key github>, <Deploy Key thomas>]
        >>> ppaas.DeployKey('github').delete()
        >>> ppaas.DeployKey.get_deploy_keys()
        [<Deploy Key thomas>]

        .. warnings:: This action is irreversible.
        """
        result, status = self.client.delete('/deploy-keys/%s' % (self.name))
        return result

    def __repr__(self):
        """String representation of the object"""
        return "<Deploy Key %s>" % (self.name)

    def __getattr__(self, name):
        """Retrieves an attribute of the class.

        This is kind of a hack. We use the __getattr__ method to access fields of the
        json representation of the class. For instance if my class is represented by

        {
            "foo": "bar",
            "lel": true
        }

        Then obj.foo will return be "bar" eventough the property has not been defined
        in an explicit way.

        :param name: Name of the attribute you want to retrieve
        :type name: str

        :return: The value of the field
        :rtype: Any primitive type
        """
        if name in self.cached_data:
            return self.cached_data[name]
        return super(DeployKey, self).__getattr__(name)
