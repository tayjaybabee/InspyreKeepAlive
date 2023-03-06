"""

File: inspyre_keep_alive/core/config/args.py
Project: InspyreKeepAlive
Description: 

Created: 2/14/23 - 21:49:49

"""
from argparse import ArgumentParser
from inspy_logger import LEVELS as LOG_LEVELS


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
