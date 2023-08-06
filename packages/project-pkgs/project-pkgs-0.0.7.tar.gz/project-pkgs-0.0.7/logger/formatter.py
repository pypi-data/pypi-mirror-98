'''
Date: 2020-12-22 10:41:08
LastEditors: Rustle Karl
LastEditTime: 2021-03-12 12:20:38
'''
from logging import Formatter, LogRecord

from color import Color, set_color, unset_color

default_color_config = {
    'DEBUG': Color.Cyan,
    'INFO': Color.Green,
    'WARNING': Color.Yellow,
    'ERROR': Color.Red,
}


class LogFormatter(Formatter):

    def __init__(self, fmt, datefmt=None, config=None) -> None:
        super(LogFormatter, self).__init__(fmt, datefmt)
        if config is None:
            config = default_color_config
        self.config = config

    def parse_color(self, level):
        return set_color(self.config.get(level, Color.Green))

    def format(self, record: LogRecord) -> str:
        record.color = self.parse_color(record.levelname)
        record.pathname = record.pathname.replace("\\", "/")
        return unset_color(super(LogFormatter, self).format(record))
