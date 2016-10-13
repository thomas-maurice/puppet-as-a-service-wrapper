#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple pythonic interface to OVH's Puppet as a Service Lab"""

__author__  = "Thomas Maurice <thomas@maurice.fr>"
__version__ = "0.0.4"
__credits__ = ["Thomas Maurice", "Balthazar Rouberol", "Romain Beuque"]
__status__  = "Developpement"
__license__ = """
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

from .master import Master
from .certificate import Certificate
from .deploy_key import DeployKey
from .client import ApiClient
