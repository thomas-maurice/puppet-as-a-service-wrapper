# Puppet as a service API wrapper

[![Build Status](https://travis-ci.org/thomas-maurice/puppet-as-a-service-wrapper.svg?branch=v0.0.1)](https://travis-ci.org/thomas-maurice/puppet-as-a-service-wrapper)
[![PyPi](https://img.shields.io/pypi/dm/ppaas.svg)](https://pypi.python.org/pypi/ppaas)
[![PyPI](https://img.shields.io/pypi/v/ppaas.svg)](https://pypi.python.org/pypi/ppaas)

This is a simple python wrapper to the [Puppet aaS](https://www.runabove.com/puppet-as-a-service.xml)
API exposed by [OVH](https://ovh.com).

It should allow you to interact with the API in a more efficient and scriptable way
than using the manager.

## Install
You can install this module via pip : `pip install ppaas`

## Use example
### Basic example
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

### Playing with certificates
```
>>> master
<Puppet Master 0e85b81f-5a29-4e2b-a46c-e024049acb07>
# Get certificates by status
>>> master.get_certificates(status="SIGNATURE PENDING")
[<Agent Certificate machine-2.maurice.fr@0e85b81f-5a29-4e2b-a46c-e024049acb07>, <Agent Certificate machine-1.maurice.fr@0e85b81f-5a29-4e2b-a46c-e024049acb07>]
>>> certs = master.get_certificates(status="SIGNATURE PENDING")
>>> cert1 = certs[0]
# Sign one !
>>> cert1.sign()
>>> cert1.status
{u'message': u'SIGNED', u'code': 1}
>>> cert1.revoke()
>>> cert1.status
{u'message': u'REVOKED', u'code': 2}
# Retrieve a certificate
>>> master.certificate('machine-2.maurice.fr')
<Agent Certificate machine-2.maurice.fr@0e85b81f-5a29-4e2b-a46c-e024049acb07>
>>> master.certificate('machine-2.maurice.fr').status
{u'message': u'REVOKED', u'code': 2}
```

### Playing with deploy keys
```
>>> ppaas.DeployKey.get_deploy_keys()
[]
>>> ppaas.DeployKey.create_deploy_key('thomas')
<Deploy Key thomas>
>>> _.public
u'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCRh1w2SJ99aqqbnGI1h0H/VBsGEhIX9cr6ASPRYCNs5pvoSljQh8u7lpb+IbcBi33YaMspyvg2kcbHIS7gP8oNe81jS3CweGTsTfgT0B8rzeGWj0lJqzVDAhiibuL3nHJ2bIdzm75bAIfmsaqX00ONnxstn18tLi0rwDt2WTKzjiz2nqNRhl/qlhcuIldlB2ZpBWOvXdpPpDbMk3Ze+4uvvdXGbTVZskyV/Tnj+GHw/t02KV9uKHJdv/FVwJwUcFnmh2DzNEtXOR2hF/5gZKXxPrrhX/s3JitJDtgdwY8ZQgElL2PWx4lepsUWbMJHBSdoWs/dvXEJfG2x2wyjnxNOHBUU3Q0t+N9He0q3IsmtPRDVh2vTqbabJQT31SchH7/0NZfxUCPImoHFIOwhQOLaDBX+9sIRAdpYvz/4U6Ep3qbb+NUIe3+zKnN2tOQ/Yvj8fRPgQcboswzN+MElVgAD2CMH6ZdJ3E3R9h9fSv/TGw4e9gCTQCS0eT3S33bIy0Bl5wmI0mByZgJrkUAYIQabS9t3eLyngHAwGhNsjA2J10W3k310Wk0moTodZgtW2V+aIpHS8814dzxg0wW1BjJXUwH4YWsVDIKTZmvCj8NQ2evZ0+b8FK2vqQv7u4+hiOP3tkQTqeq1mevpShivazjJTE3UkJr4w05YWdKcTJGN3w=='
>>> ppaas.DeployKey('thomas').delete()
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

## Contributors
 * [Thomas Maurice](https://github.com/thomas-maurice)
 * [Balthazar Rouberol](https://github.com/brouberol)
 * [Romain Beuque](https://github.com/Rbeuque74)
