# -*- coding:utf-8 -*-
"""
This is whole project logging functionality that could be used.

author: Guangqiang.lu
"""

import logging
import tempfile
import shutil
import os
from datetime import datetime

# Add with contextlib module to make the log to start and end message auto
from contextlib import contextmanager

from auto_ml.utils.CONSTANT import TMP_FOLDER

class Logger(object):
    def __init__(self, logger_name=None):
        if logger_name is None:
            logger_name = "logging"   # we could change this.
        self.logger_name = logger_name
        # self._logger_path = os.path.join(tempfile.gettempdir(), 'logging')
        self._logger_path = os.path.join(TMP_FOLDER, 'logging')
        if not os.path.exists(self._logger_path):
            try:
                os.mkdir(self._logger_path)
            except IOError as e:
                raise IOError("When try to create logging folder with error:%s" % e)

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)
        # this is to write logging info to disk
        # I just want to ensure there is only one logging file in current folder,
        # after the whole process finish, I just upload the file to HDFS for later use case
        self.logger_file_name = 'logging_%s.log' % datetime.now().strftime('%Y%m%d')
        self.logger_file_path = os.path.join(self._logger_path, self.logger_file_name)

        file_handler = logging.FileHandler(self.logger_file_path)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        # this is to write the logging info to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(file_handler)
        self._file_handler = file_handler

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def exception(self, msg):
        self.logger.exception(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def save_log_file(self, save_file_path):
        """
        To save the logger file into that folder,
        default will remove logger folder when call this func.
        :param save_file_path: Which folder to save
        :return:
        """
        try:
            # first we need to close the file writer
            self._file_handler.close()
            self.logger.removeHandler(self._file_handler)
        except Exception as e:
            raise IOError("When try to close file writer with error: {}".format(e))

        # then let's move the file into that folder
        try:
            shutil.move(self.logger_file_path, os.path.join(save_file_path, self.logger_file_name))
            # then just remove the tmp folder, as this function should be called only after whole step finish
            shutil.rmtree(self._logger_path)
        except IOError as e:
            raise IOError("When try to move logger file into {} with error: {}".format(save_file_path, e))


# def create_logger():
#     logger = Logger()

#     return logger

@contextmanager
def create_logger_context(logger_name):
    logger = Logger(logger_name)

    logger.info("Start logging for `{}`".format(logger_name))
    yield logger
    # logger.info("End logging for {}".format(logger_name))


def create_logger(logger_name=None):
    """Create a logger obj to log info for starting log"""
    if logger_name is None:
        logger_name = "logger"

    if os.path.isfile(logger_name):
        # in case that we provide with __file__ attr, then just with file name. 
        # so that we could get better insight.
        logger_name = os.path.basename(logger_name)

    with create_logger_context(logger_name) as logger:
        return logger

# logger = create_logger()

if __name__ == '__main__':
    logger = create_logger()
    logger.info("test")
    logger.warning("This is warning")

    logger2 = create_logger("test")
    logger2.info("new logger")