import logging
import sys
from datetime import datetime
from logging import LogRecord, Logger
from typing import Optional

import colorlog
import pytz


class TimestampFormatter(colorlog.ColoredFormatter):
    # NOTE: colorlog.ColoredFormatter is inherited from logging.Formatter

    # override the class member, converter, in logging.Formatter
    converter = datetime.fromtimestamp

    def __init__(self, fmt: Optional[str], timezone: str = "UTC", sub_sec_unit: str = "microseconds"):
        """

        Args:
            fmt (Optional[str]): format style of logging
                                 - (see: https://docs.python.org/3/library/logging.html#logrecord-attributes)
                                 - NOTE: no need to use %(msecs)d in this overridden method

            timezone (str): timezone (default: UTC)
                            (checkout pytz.all_timezones)

            sub_sec_unit (str): Either display "milliseconds" or "microseconds"
                                (default: "microseconds")

        """
        super().__init__(fmt)
        self.__timezone = timezone
        self.__sub_sec_unit = sub_sec_unit

    def formatTime(self, record: LogRecord, datefmt: Optional[str] = None) -> str:
        """
        Override formatTime method in logging.Formatter to generate ISO8601 Timestamp,
        with (milliseconds or microseconds) and timezone

        Args:
            record (LogRecord): a LogRecord instance

            datefmt (Optional[str]): date format (not used here)

        Returns:
            (str): ISO8601 Timestamp with milliseconds or microseconds and timezone

        """
        _timestamp = self.converter(record.created, tz=pytz.timezone(self.__timezone))

        return _timestamp.isoformat(timespec=self.__sub_sec_unit)


def get_logger(module_name: str, level: str = "DEBUG") -> Logger:
    """
    Return a logger
    Args:
        module_name (str): module name. Typically, you will use __name__

        level (str): messages will be logged only if >= level  (default: "DEBUG")
                     (e.g. "DEBUG", "INFO", "WARNING", "ERROR")

    Returns:
        (Logger): a logger instance

    """
    logger = logging.getLogger(module_name)
    logger.setLevel(level=level)

    handler = colorlog.StreamHandler(sys.stdout)

    format_style = "%(log_color)s %(asctime)s | %(levelname)s | %(message)s"
    formatter = TimestampFormatter(fmt=format_style)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
