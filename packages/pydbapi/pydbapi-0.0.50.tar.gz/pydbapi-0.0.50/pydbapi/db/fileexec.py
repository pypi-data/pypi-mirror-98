# @Author: chunyang.xu
# @Email:  398745129@qq.com
# @Date:   2020-06-08 11:55:54
# @Last Modified time: 2021-03-03 19:16:38
# @github: https://github.com/longfengpili

# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time

from .base import DBbase
from pydbapi.sql import SqlFileParse

import logging
import logging.config
from pydbapi.conf import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
dblogger = logging.getLogger('db')


class DBFileExec(DBbase):

    def __init__(self):
        super(DBFileExec, self).__init__()

    def get_filesqls(self, filepath, **kw):
        sqlfileparser = SqlFileParse(filepath)
        arguments, sqls = sqlfileparser.get_filesqls(**kw)
        return arguments, sqls

    def file_exec(self, filepath, **kw):
        st = time.time()
        results = {}
        filename = os.path.basename(filepath)
        dblogger.info(f"Start Job 【{filename}】".center(80, '='))
        arguments, sqls = self.get_filesqls(filepath, **kw)
        dblogger.info(f"【Final Arguments】The file 【{filename}】 Use arguments {arguments}")
        for desc, sql in sqls.items():
            dblogger.info(f">>> START {desc}")
            verbose = 1 if 'verbose1' in desc or filename.startswith('test') \
                else 2 if 'verbose2' in desc else 0
            rows, action, result = self.execute(sql, verbose=verbose)
            results[desc] = result
            # dblogger.info(f"End {desc}")
        et = time.time()
        dblogger.info(f"End Job 【{filename}】, cost {et - st:.2f} seconds".center(80, '='))
        return results
