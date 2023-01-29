import logging
from time import strftime
from os import path
from typing import Optional

from src.parsers.settings_parser import app_settings


class Logger:

    def __init__(self,
                 name: str,
                 info_path: str) -> None:
        self._logger = logging.getLogger(name)
        self._file_handler = None
        self._stream_handler = None
        if app_settings().parameters().logging_enabled():
            self._file_handler = logging.FileHandler(info_path, mode="w")
            self._stream_handler = logging.StreamHandler()
            self._file_handler.setLevel(logging.INFO)
            self._stream_handler.setLevel(logging.INFO)
            self._logger.addHandler(self._file_handler)
            self._logger.addHandler(self._stream_handler)


    def info(self,
             msg,
             *args,
             **kwargs) -> None:
        if app_settings().parameters().logging_enabled():
            self._logger.warning(msg, *args, **kwargs)

    def error(self,
              msg,
              *args,
              **kwargs) -> None:
        if app_settings().parameters().logging_enabled():
            self._logger.error(msg, *args, **kwargs)

    def exception(self,
                  msg,
                  *args,
                  **kwargs) -> None:
        if app_settings().parameters().logging_enabled():
            self._logger.exception(msg, *args, **kwargs, exc_info=True)


_logger_instances = dict()


def logger(name: Optional[str] = __name__) -> Logger:
    global _logger_instances
    if name not in _logger_instances:
        log_name = path.join(app_settings().paths().log_dir(),
                             str(strftime("%m-%d-%Y_%H-%M-%S")) + '_log.txt')
        _logger_instances[name] = Logger(name, log_name)

    return _logger_instances[name]
