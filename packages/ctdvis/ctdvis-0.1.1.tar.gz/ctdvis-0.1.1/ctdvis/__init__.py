# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-07-03 11:33

@author: a002028

"""
import sys
import os
import json
from pkg_resources import get_distribution, DistributionNotFound


name = "ctdvis"

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

from ctdvis import callbacks
from ctdvis import readers
from ctdvis import sources
from ctdvis import widgets
# package_path = os.path.dirname(os.path.realpath(__file__))
# package_path = package_path.replace('ctdvis\\ctdvis', 'ctdvis')
#
# pypaths_path = package_path + '\\pypaths.json'
#
#
# def append_path_to_system(item):
#     """"""
#     if isinstance(item, str):
#         if item not in sys.path:
#             if os.path.isdir(item):
#                 sys.path.append(item)
#             else:
#                 print('\nWARNING! Could not add "{}" to sys.path. \n'
#                       'You should probably change path to the py-package "{}" in '
#                       'settingsfile: {}\n'.format(item, os.path.basename(item), pypaths_path))
#     elif isinstance(item, list):
#         for it in item:
#             append_path_to_system(it)
#     elif isinstance(item, dict):
#         for k, it in item.items():
#             append_path_to_system(it)
#
#
# def append_python_paths():
#     if os.path.isfile(pypaths_path):
#         with open(pypaths_path, 'r') as fd:
#             d = json.load(fd)
#         append_path_to_system(d)
#
#
# append_python_paths()


