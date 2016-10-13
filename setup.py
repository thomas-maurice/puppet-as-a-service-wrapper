#!/usr/bin/env python

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

setup(
    name='ppaas',
    version='0.0.4',
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
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'requests==2.9.1',
    ],
    license="WTFPL",
)
