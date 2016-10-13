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

import json

from .client import ApiClient
from .certificate import Certificate


def pretty_print(d):
    """Prints json in a cool and indented way

    :param d: The dictionary to prettify
    :type d: dict

    :return: A pretty string version of d
    :rtype: str
    """
    return json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))


class Master(object):
    """Interface for the /masters/<masterId> endpoints.

    This class allows you to interract with your Puppet Masters

    This class has the following behavior:
      * When loaded it will cache some data in self.cached_data (it will
        cache its json representation according to the API)
      * Everytime you want to get data from the object, like certificate.fingerprint,
        the cache will be used, so make sure to call reload_datas if updates has been done.
      * Dictionnary lookup is done via the __getattr__ overloaded method. It
        is a bit hacky but it does the job. For instance to get the hostname
        of your master, you can type `master.hostname`, this will query the
        cached value in the object


    An example json representation of what this class may look like :
    .. code-block:: json
        {
            "allowed_networks": [
                "0.0.0.0/0"
            ],
            "ca_certificate": "-----BEGIN [.]CATE-----",
            "created_at": "2015-12-07T13:28:28",
            "deploy_key": "github",
            "hierarchy": [],
            "hieras": [],
            "hostname": "master1.user.puppet.runabove.io",
            "id": "1e42115b-34f9-4f86-a4a7-67e30a24a825",
            "name": "master1",
            "nb": 1,
            "servers": {},
            "source": "git@github.com:puppet/puppet.git",
            "status": {
                "code": 0,
                "msg": "Deploying server"
            },
            "token": "d4K1cxIPklE",
            "type": "eg-7",
            "vars": {}
        }
    """
    def __init__(self, uuid, cached_data=None):
        """Creates a new object representing an *existing* puppet master

        :param uuid: UUID of the master
        :type uuid: str
        :param cached_data: Cached data to instantiate the master
        :type cached_data: dict


        :Example:
        >>> ppaas.Master('0e85b81f-5a29-4e2b-a46c-e024049acb07')
        <Puppet Master 0e85b81f-5a29-4e2b-a46c-e024049acb07>
        >>> master.name
        'thomas'

        .. seealso:: get_masters()
        """
        self.client = ApiClient()
        self.uuid = uuid
        self.reload_data(cached_data)

    def reload_data(self, refreshed_datas=None):
        """Reloads datas in the cached_data properties of the pupet master

        :param refreshed_datas: Data to use to reload cached_data property of master
        :type refreshed_datas: dict

        """
        if refreshed_datas:
            self.cached_data = refreshed_datas
        else:
            self.cached_data, _ = self.client.get('/masters/%s' % self.uuid)

    @staticmethod
    def create_master(name, source, deploy_key, vars={}, nb=1, type=None, hierarchy=[], hieras=[], client=None):
        """ Creates a Pupper master

        :param name: Name of the puppet master
        :type name: str
        :param source: Source git repository of the puppet master
        :type source: str
        :param deploy_key: Deploy key to link with your puppet master
        :type deploy_key: ppaas.DeployKey
        :param nb: Number of servers for the master
        :type nb: int
        :param type: Kind of server to use
        :type type: str
        :param hierarchy: Array of hierarchies
        :type hierarchy: list
        :param hieras: Array of hiera backend
        :type hieras: list
        :param client: A client object you want to pass, if empty a new one will be created
        :type client: ppaas.ApiClient

        :return: The newly created puppet master
        :rtype: Master

        :Example:
        >>> ppaas.Master.create_master("master1", "git@github.com:puppet/puppet.git", "github")
        <Puppet Master 0e85b81f-5a29-4e2b-a46c-e024049acb07>
        >>> master.name
        'master1'

        """
        payload = {"name": name, "source": source, "deploy_key": deploy_key, "nb": nb,
                   "hierarchy": hierarchy, "hieras": hieras, "vars": vars}
        if type:
            payload["type"] = type

        if not client:
            client = ApiClient()

        result, _ = client.post("/masters", data=payload)
        return Master(result["id"], result)

    @staticmethod
    def get_masters(client=None):
        """Retrieves all your puppet masters

        :param client: A client object you want to pass, if empty a new one will be created
        :type client: ppaas.ApiClient

        :return: The list of your puppet masters
        :rtype: List of Master objects

        :Example:

        >>> ppaas.Master.get_masters()
        [<Puppet Master 0e85b81f-5a29-4e2b-a46c-e024049acb07>]
        """
        if not client:
            client = ApiClient()
        result, status = client.get('/masters')
        masters = []
        for master in result['masters']:
            masters.append(Master(master['id'], master))
        return masters

    @staticmethod
    def get_master(name, client=None):
        """Gets a master by name, because who the hell can remember uuids ?

        :param name: Name of the Puppet Master you want to retrieve
        :param client: A client object you want to pass, if empty a new one will be created
        :type name: str
        :type client: ppaas.ApiClient

        :return: A Master object, or None if no matching master was found
        :rtype: ppaas.Master, or None

        :Example:

        >>> ppaas.Master.get_master('thomas')
        <Puppet Master 0e85b81f-5a29-4e2b-a46c-e024049acb07>
        """
        if not client:
            client = ApiClient()
        masters = Master.get_masters(client)
        for master in masters:
            if master.cached_data['name'] == name:
                return master
        return None

    def get_certificates(self, status=None):
        """Returns all the certificates attached to a master

        Optionally you can specify a `status` for the certificates. The statuses can either be
          * "SIGNATURE PENDING"
          * "SIGNED"
          * "REVOKED"
        If status is None, all the certifictes will be returned regardless of their status

        Note that it is just for conveinence that this option is provided. From the API's point
        of view we will issue the same request anyway.

        :param status: The status of the certificates
        :type status: str

        :return: A list of matching certificates
        :rtype: List of ppaas.Certificate

        """
        certificates = Certificate.get_certificates(self, self.client)
        if status is None:
            return certificates
        else:
            return [cert for cert in certificates if cert.status['message'] == status]

    def __repr__(self):
        """String representation of the object"""
        return "<Puppet Master %s>" % self.uuid

    def refresh(self):
        """Asks the master to refresh itself.

        You usually want to do it to trigger the pull of your git repository

        :return: Wether the refresh has been accepted
        :rtype: boolean

        .. note:: The API can answer False if a refresh is already in progress.
        """
        try:
            self.client.post('/masters/%s/refresh' % self.uuid)
            return True
        except:
            return False

    def restart(self):
        """Asks the master to restart

        You usually want to do it when you have edited your hiera or your
        custom puppet functions

        :return: Wether the restart has been accepted
        :rtype: boolean
        """
        try:
            self.client.post('/masters/%s/restart' % self.uuid)
            return True
        except:
            return False

    def certificate(self, hostname):
        """Returns the certificate of a particular hostname

        :param hostname: The hostname you want the certificate of
        :type hostname: str

        :return: The ppaas.Certificate object, or raises an exception
        :rtype: ppaas.Certificate
        """
        return Certificate(self, hostname)

    @property
    def crl(self):
        """Gets the CRL of the master

        :return: The CRL
        :rtype: str
        """
        data, result = self.client.get('/masters/%s/crl' % self.uuid)
        return data['crl']

    @property
    def certificates(self):
        """Gets all the certificates of the master

        :return: The list of the certificates
        :rtype: List of dicts !!!

        .. warnings:: Does not return an object, but a dict
        """
        data, result = self.client.get('/masters/%s/certs' % self.uuid)
        return data['certs']

    @property
    def environments(self):
        """Gets the environments

        It can look like :
        .. code-block:: json
            {
                "environments": {
                    "production": {
                        "settings": {
                            "config_version": "",
                            "environment_timeout": 0,
                            "manifest": "environments/production/manifests",
                            "modulepath": [
                                "/etc/puppet/environments/production/modules",
                                "/etc/puppet/modules",
                                "/usr/share/puppet/modules"
                            ]
                        }
                    }
                }
            }

        :return: The environments of the master
        :rtype: dictionary
        """
        data, result = self.client.get('/masters/%s/environments' % self.uuid)
        return data['environments']

    @property
    def last_update(self):
        """Gets the last update of the master

        Can look like: "2015-12-07T13:28:28"

        :return: Last master update
        :rtype: str
        """
        data, result = self.client.get('/masters/%s/last-update' % self.uuid)
        return data['result']

    def to_dict(self):
        """Returns the JSON representation of the object"

        :return: A dictionary containing the object as served by the API
        :rtype: dict
        """
        result, status = self.client.get('/masters')
        return result

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
        return super(Master, self).__getattr__(name)
