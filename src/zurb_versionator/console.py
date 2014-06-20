#!/usr/bin/env python3

'''
@author: Arkadiusz Dzięgiel
'''

import subprocess
import json
from verlib import NormalizedVersion as V, suggest_normalized_version
from collections import OrderedDict
from urllib.request import urlopen
import urllib
import os
import logging
from itertools import zip_longest
from logging.handlers import SysLogHandler
from bottle import Bottle
import traceback
