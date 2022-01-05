import sys
import logging

from datetime import date
from logging import handlers
from utils import ensure_dir

root_dir = 'logs/'
ensure_dir(root_dir)


def get_logger(log_name, max_log_file_in_mb=15, logger_name='default'):
    """
    Get logging and format
    All logs will be saved into logs/log-DATE (default)
    Default size of log file = 15m
    :param log_name:
    :param max_log_file_in_mb:
    :param logger_name:
    :return:
    """
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(log_format)
    log.addHandler(ch)

    if '/' in log_name:
        fh = handlers.RotatingFileHandler(
            log_name + '-' + str(date.today()),
            maxBytes=(1024*1024)*max_log_file_in_mb,
            backupCount=12
        )
    else:
        fh = handlers.RotatingFileHandler(
            root_dir + log_name + '-' + str(date.today()),
            maxBytes=(1024 * 1024) * max_log_file_in_mb,
            backupCount=12
        )

    fh.setFormatter(log_format)
    log.addHandler(fh)

    return log


info_log = get_logger(root_dir + 'info.log', 25, logger_name='info')
error_log = get_logger(root_dir + 'error.log', 25, logger_name='error')
