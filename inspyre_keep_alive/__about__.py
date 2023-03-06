"""

File: inspyre_keep_alive/__about__.py
Project: InspyreKeepAlive
Description: 

Created: 2/14/23 - 21:50:23

"""
import os
from appdirs import user_config_dir

__AUTHOR__ = 'Inspyre Softworks'

__PROG__ = 'InspyreKeepAlive'

__VERSION__ = '0.1_a1'

__DESCRIPTION__ = 'Keep your screen alive.'

DEFAULT_CONF_DIR = os.path.join(user_config_dir(appname=__PROG__, appauthor=__AUTHOR__))
