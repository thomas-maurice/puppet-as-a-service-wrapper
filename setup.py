#!/usr/bin/env python

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

setup(
    name='ppaas',
    version='0.0.2',
    description="Interface for OVH's Puppet as a service lab",
    long_description=readme,
    author='Thomas Maurice',
    author_email='thomas@maurice.fr',
    url='https://github.com/thomas-maurice/puppet-as-a-service-wrapper',
    packages=['ppaas'],
    platforms='any',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
	'cffi==1.5.2',
	'cryptography==1.2.2',
	'enum34==1.1.2',
	'idna==2.0',
	'ipaddress==1.0.16',
	'ndg-httpsclient==0.4.0',
	'pyasn1==0.1.9',
	'pycparser==2.14',
	'pyOpenSSL==0.15.1',
	'requests==2.9.1',
	'six==1.10.0',
	'wheel==0.26.0',
    ], 
    license="WTFPL",
)
