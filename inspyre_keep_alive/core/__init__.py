"""

File: inspyre_keep_alive/core/__init__.py
Project: InspyreKeepAlive
Description: 

Created: 2/14/23 - 21:49:26

"""

from inspy_logger import InspyLogger
from inspyre_keep_alive.__about__ import __PROG__ as PROG_NAME
from inspyre_keep_alive.core.config.args import PARSED_ARGS


ISL = InspyLogger(PROG_NAME, PARSED_ARGS.log_level)


if not ISL.device.started:
    log = ISL.device.start()
    log.info(f'Main logger for {PROG_NAME} started.')
