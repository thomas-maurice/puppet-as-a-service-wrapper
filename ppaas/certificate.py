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


class Certificate(object):
    """Interface for the /masters/<masterId>/certs endpoints.

    This class allows you to interract with your agent certificates.

    This class has the following behavior:
      * When loaded it will cache some data in self.cached_data (it will
        cache its json representation according to the API)
      * Everytime you want to get data from the object, like certificate.fingerprint,
        the cache will be used, so make sure to call reload_datas if updates has been done.
      * Dictionnary lookup is done via the __getattr__ overloaded method. It
        is a bit hacky but it does the job. For instance to get the fingerprint
        of your certificate, you can type `cert.fingerprint`, this will query the
        cached value in the object

    An example json representation of what this class may look like :
    .. code-block:: json
        {
            "created_at": "2015-12-07T13:28:28",
            "fingerprint": "A7:DA:BE:17:09:9E:18:7D:E6:24:25:7C:65:48:EF",
            "hostname": "web.domain.tld",
            "revoked_at": null,
            "serial_number": null,
            "signed_at": null,
            "status": {
                "code": 0,
                "message": "SIGNATURE PENDING"
            }
        }
    """
    def __init__(self, master, hostname, cached_data=None):
        """Creates a new object representing an *existing* agent certificate

        :param master: The Master the wanted certificate is attached to
        :type master: ppaas.Master
        :param hostname: The hostname of the agent
        :type hostname: str
        :param cached_data: Cached data to instantiate the master
        :type cached_data: dict

        :Example:
        >>> ppaas.Master.get_masters()
        [<Puppet Master 0e85b81f-5a29-4e2b-a46c-e024049acb07>]
        >>> master = _[0]
        >>> ppaas.Certificate(master, 'machine.maurice.fr')
        <Agent Certificate machine.maurice.fr@0e85b81f-5a29-4e2b-a46c-e024049acb07>

        .. note:: You will probably never call this directly and instead use the
                  ppaas.Master.certificate() method instead
        .. seealso:: get_certificates(), ppaas.Master.certificate()
        """
        self.client = ApiClient()
        self.hostname = hostname
        self.master = master
        self.reload_data(cached_data)

    def reload_data(self, refreshed_datas=None):
        """Reloads datas in the cached_data properties of a certificate

        :param refreshed_datas: Data to use to reload cached_data property of certificate
        :type refreshed_datas: dict

        """
        if refreshed_datas:
            self.cached_data = refreshed_datas
        else:
            self.cached_data, _ = self.client.get('/masters/%s/certs/%s' % (self.master.uuid, self.hostname))

    @staticmethod
    def get_certificates(master, client=None):
        """Returns all the agent certificates for a Master

        :param master: The master in question
        :param client: The ApiClient to use
        :type master: ppaas.Master
        :type client: ppaas.ApiClient

        :Example:

        >>> ppaas.Master.get_masters()
        [<Puppet Master 0e85b81f-5a29-4e2b-a46c-e024049acb07>]
        >>> master = _[0]
        >>> ppaas.Certificate.get_certificates(master)
        [<Agent Certificate machine.maurice.fr@0e85b81f-5a29-4e2b-a46c-e024049acb07>]

        .. note:: You will probably never use this method neither and use the one
                  shipped with the Master class I guess.
        """
        if not client:
            client = ApiClient()
        result, status = client.get('/masters/%s/certs' % master.uuid)
        certificates = []
        for certificate in result['certs']:
            certificates.append(Certificate(master, certificate['hostname'], certificate))
        return certificates

    def to_dict(self):
        """Returns the JSON representation of the object"

        :return: A dictionary containing the object as served by the API
        :rtype: dict

        :Example:

        >>> ppaas.Certificate(master, 'machine.maurice.fr').to_dict()
        {u'revoked_at': None, u'signed_at': None, u'created_at': u'2016-02-21T11:21:58', u'hostname': u'machine.maurice.fr', u'status': {u'message': u'SIGNATURE PENDING', u'code': 0}, u'fingerprint': u'9F:1F:B2:C6:8F:D2:62:26:7B:A3:49:00:45:6F:D6:81:3A:28:D8:ED:42:C4:23:F6:FF:82:64:F9:60:7F:36:9B', u'serial_number': None}
        """
        result, status = self.client.get('/masters/%s/certs/%s' % (self.master.uuid, self.hostname))
        return result

    def delete(self):
        """Deletes a certificate.

        If the certificate has not been revoked yet it will be revoked and deleted.

        :return: None, or raises an exception
        :rtype: None
        """
        result, status = self.client.delete('/masters/%s/certs/%s' % (self.master.uuid, self.hostname))
        return result

    def revoke(self):
        """Revokes a certificate.

        :return: None, or raises an exception
        :rtype: None
        """
        result, status = self.client.post('/masters/%s/certs/%s/revoke' % (self.master.uuid, self.hostname))
        self.reload_data()
        return result

    def sign(self):
        """Signes a certificate.

        :return: None, or raises an exception
        :rtype: None
        """
        result, status = self.client.post('/masters/%s/certs/%s/sign' % (self.master.uuid, self.hostname))
        self.reload_data()
        return result

    def __repr__(self):
        """String representation of the object"""
        return "<Agent Certificate %s@%s>" % (self.hostname, self.master.uuid)

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
        return super(Certificate, self).__getattr__(name)
