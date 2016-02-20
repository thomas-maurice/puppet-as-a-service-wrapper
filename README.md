# Puppet as a service API wrapper

This is a simple python wrapper to the [Puppet aaS](https://www.runabove.com/puppet-as-a-service.xml)
API exposed by [OVH](https://ovh.com).

It should allow you to interact with the API in a more efficient and scriptable way
than using the manager.

## Use example

```
>>> import ppaas
>>> masters = ppaas.Master.get_masters()
>>> masters
[<Puppet Master 0e85b81f-5a29-4e2b-a46c-e024049acb07>]
>>> main = masters[0]
>>> main.get_certificates()
[<Agent Certificate 064a859fff81@0e85b81f-5a29-4e2b-a46c-e024049acb07>]
>>> main.get_certificates()[0].to_dict()
{u'revoked_at': None, u'signed_at': None, u'created_at': u'2016-02-19T18:52:37', u'hostname': u'064a859fff81', u'status': {u'message': u'SIGNATURE PENDING', u'code': 0}, u'fingerprint': u'C4:1C:BD:FD:9D:8C:30:45:84:AE:FA:3F:89:EC:6F:59:BE:8C:CA:C7:55:33:9C:44:BF:29:7F:73:0B:27:1C:DE', u'serial_number': None}
>>> main.refresh()
True
```

## Credentials
This module will look for a credential files in the following places :
* ./ppaas.conf
* ~/.ppaas.conf
* /etc/ppaas.conf

This file should look like:
```
[auth]
user=my_user_name
pass=my_password

[api]
endpoint=https://puppet.runabove.io
```

## Contributing
Feel free to contribute by submitting PRs ! The documentation for the API can be found
[here](https://puppet.runabove.io/doc/index.html)
