#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/22 15:09
# @Author  : qidl
# @Software: PyCharm

import os
import time
import logging
import config as cfg

def make_dir(log_path):
    path = log_path.strip()

    if not os.path.exists(path):
        os.makedirs(path)
    return path

log_dir_name = cfg.Config.LOG_DIR_NAME
log_file_name = 'risk_' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'

log_file_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
) + os.sep + log_file_name

make_dir(log_file_dir)

log_file_str = log_file_dir + os.sep + log_file_name
log_level = cfg.Config.LOG_LEVEL

handler = logging.FileHandler(log_file_str, encoding='UTF-8')

handler.setLevel(log_level)

logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
)

handler.setFormatter(logging_format)
