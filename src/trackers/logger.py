""" This module provides logging to the app.
"""

from logging import FileHandler, getLogger, INFO, StreamHandler
from os import path
from time import strftime
from typing import Optional

from src.parsers.settings_parser import app_settings


class Logger:
    """ This class builds upon the logging api and
        provides a seamless way to perform logging throughout
        the app. """

    def __init__(self,
                 name: str,
                 info_path: str) -> None:
        self._logger = getLogger(name)
        self._file_handler = None
        self._stream_handler = StreamHandler()
        self._stream_handler.setLevel(INFO)
        self._logger.addHandler(self._stream_handler)

        # only print to log file if enabled
        if app_settings().parameters().logging_enabled():
            self._file_handler = FileHandler(info_path, mode="w")
            self._file_handler.setLevel(INFO)
            self._logger.addHandler(self._file_handler)

    def info(self,
             msg,
             *args,
             **kwargs) -> None:
        """ Simple api for reporting info level logging. The logging
            module for some reason doesn't print out info level, however,
            warning does. """

        self._logger.warning(msg, *args, **kwargs)

    def error(self,
              msg,
              *args,
              **kwargs) -> None:
        """ Forwards the error to the logging module. """

        self._logger.error(msg, *args, **kwargs)

    def exception(self,
                  msg,
                  *args,
                  **kwargs) -> None:
        """ Forwards the exception to the logging module. """

        self._logger.exception(msg, *args, **kwargs, exc_info=True)


_logger_instances = dict()


def logger(name: Optional[str] = __name__) -> Logger:
    """ Singleton accessor for this class. """

    global _logger_instances
    if name not in _logger_instances:
        log_name = path.join(app_settings().paths().log_dir(),
                             str(strftime("%m-%d-%Y_%H-%M-%S"))
                             + '_log.txt')
        _logger_instances[name] = Logger(name, log_name)

    return _logger_instances[name]
