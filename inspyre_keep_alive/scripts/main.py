"""

File: inspyre_keep_alive/scripts/main.py
Project: InspyreKeepAlive
Description: 

Created: 2/14/23 - 21:57:25

"""
from inspyre_keep_alive.core.config.args import PARSED_ARGS


# /usr/bin/env python3

# keep_alive.py keeps the screen active by pressing and releasing the
# 'Ctrl' key every n seconds

from argparse import ArgumentParser
from inspy_logger import InspyLogger as ISL, LEVELS as LOG_LEVELS
import keyboard
from time import sleep
import time
from threading import Timer

LOG_NAME = 'KeepAlive'


class Arguments(ArgumentParser):
    __parsed = None

    def __init__(self, *args, **kwargs):
        super(Arguments, self).__init__(*args, **kwargs)

        self.description = 'A simple keyboard input simulator to keep your screen alive.'
        self.add_argument(
            '-i',
            '--interval',
            help='The number of seconds between presses of the key',
            default=5,
            action='store',
            required=False
        )
        self.add_argument(
            '-k',
            '--key',
            help='The key to press every n seconds',
            default='Ctrl',
            action='store',
            required=False
        )

        self.add_argument(
            '-l',
            '--log-level',
            help='The level at which to log.',
            choices=LOG_LEVELS,
            default='debug'
        )

    @property
    def as_dict(self):
        return {
                'interval': self.interval,
                'log_level': self.log_level,
                'key': self.key
        }

    @property
    def parsed(self):
        if self.__parsed is None:
            self.__parsed = self.parse_args()

        return self.__parsed

    @property
    def interval(self):
        return self.parsed.interval

    @property
    def key(self):
        return self.parsed.key

    @property
    def log_level(self):
        return self.parsed.log_level

    def __str__(self):
        _ = 'Arguments'
        for k, v in self.as_dict.items():
            _ += f'\n    {k}: {v}'.ljust(4)

        return _



ARGUMENTS = Arguments()
PARSED_ARGS = ARGUMENTS.parsed

### End Argument Section ###
############################
###    Begin real code   ##


# Set up logger
MAIN_LOG = ISL('KeepAlive', PARSED_ARGS.log_level)
LOG = MAIN_LOG.device.start()

LOG.debug('Starting KeepAlive')
LOG.debug('Logging started')


# Set up timer pointer
timer = None

iterations = 0


def keep_alive(key=ARGUMENTS.key, interval=ARGUMENTS.interval):
    """
    Press the provided key every n seconds in an effort to keep the screen alive.

    Args:
        key (str):
            The key to press when the interval is reached.

        interval ((int|float), optional):
            The number of seconds to wait between key-presses.:

    Returns:
        None

    """
    global timer, iterations

    iterations += 1

    log = MAIN_LOG.device.add_child(f'{LOG_NAME}.keep_alive')
    log.debug(f'keep_alive iteration #{iterations}')

    keyboard.press_and_release(key)
    log.debug(f'Pressed {key}')

    timer = Timer(interval=interval, function=keep_alive)
    timer.daemon = True
    timer.name = f'keep_alive_{iterations}'
    timer.start()


def listener():
    log = MAIN_LOG.device.add_child(f'{LOG_NAME}.listener')
    log.debug('Setting up quit key-combo')
    keyboard.add_hotkey('ctrl+shift+q', quit, args=(['User pressed key combination']))
    log.debug('Hotkey setup')

def quit(reason=None):
    global timer

    log = MAIN_LOG.device.add_child(f'{LOG_NAME}.quit')

    log.debug('Quitting')
    if reason is not None:
        log.debug(f'Reason: {reason}')

    timer.cancel()


timer = Timer(PARSED_ARGS.interval, keep_alive, args=[PARSED_ARGS.key, PARSED_ARGS.interval])

timer.daemon = True
listener()
timer.start()
