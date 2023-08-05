# @Author: chunyang.xu
# @Email:  398745129@qq.com
# @Date:   2020-06-10 14:40:50
# @Last Modified time: 2021-03-10 17:40:28
# @github: https://github.com/longfengpili

# !/usr/bin/env python3
# -*- coding:utf-8 -*-


import threading
import pymysql

from pydbapi.db import DBCommon, DBFileExec
from pydbapi.sql import SqlCompile
from pydbapi.conf import AUTO_RULES


import logging
import logging.config
from pydbapi.conf import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
mysqllogger = logging.getLogger('mysql')


class SqlMysqlCompile(SqlCompile):
    '''[summary]

    [description]
        构造mysql sql
    Extends:
        SqlCompile
    '''

    def __init__(self, tablename):
        super(SqlMysqlCompile, self).__init__(tablename)

    def create(self, columns, indexes):
        'mysql 暂不考虑索引'
        sql = self.create_nonindex(columns)
        # if indexes and not isinstance(indexes, list):
        #     raise TypeError(f"indexes must be a list !")
        # if indexes:
        #     indexes = ','.join(indexes)
        #     sql = f"{sql.replace(';', '')}interleaved sortkey({indexes});"
        return sql

    def dumpsql(self, columns, dumpfile, fromtable=None, condition=None):
        selectsql = self.select_base(columns, fromtable=fromtable, condition=condition)
        intosql = f'into outfile "{dumpfile}" fields terminated by ",";'
        dumpsql = selectsql.replace(";", intosql)
        return dumpsql

    def loadsql(self, columns, loadfile, intotable=None):
        intotable = intotable or self.tablename
        loadsql = f'load data infile "{loadfile}" into table {intotable} fields terminated by "," ({columns.select_cols});'
        return loadsql


class MysqlDB(DBCommon, DBFileExec):
    _instance_lock = threading.Lock()

    def __init__(self, host, user, password, database, port=3306, charset="utf8", safe_rule=True):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        super(MysqlDB, self).__init__()
        self.auto_rules = AUTO_RULES if safe_rule else None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(MysqlDB, '_instance'):
            with MysqlDB._instance_lock:
                if not hasattr(MysqlDB, '_instance'):
                    MysqlDB._instance = MysqlDB(*args, **kwargs)

        return MysqlDB._instance

    def get_conn(self):
        conn = pymysql.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port, charset=self.charset)
        if not conn:
            self.get_conn()
        return conn

    def create(self, tablename, columns, indexes=None, verbose=0):
        # tablename = f"{self.database}.{tablename}"
        sqlcompile = SqlMysqlCompile(tablename)
        sql_for_create = sqlcompile.create(columns, indexes)
        rows, action, result = self.execute(sql_for_create, verbose=verbose)
        return rows, action, result

    def dumpdata(self, tablename, columns, dumpfile, condition=None, verbose=0):
        sqlcompile = SqlMysqlCompile(tablename)
        sql_for_dump = sqlcompile.dumpsql(columns, dumpfile, condition=condition)
        rows, action, result = self.execute(sql_for_dump, verbose=verbose)
        mysqllogger.info(f"【{action}】{tablename} dumpdata {rows} rows succeed, outfile: {dumpfile} !")
        return rows, action, result

    def loaddata(self, tablename, columns, loadfile, verbose=0):
        sqlcompile = SqlMysqlCompile(tablename)
        sql_for_load = sqlcompile.loadsql(columns, loadfile)
        rows, action, result = self.execute(sql_for_load, verbose=verbose)
        mysqllogger.info(f"【{action}】{tablename} loaddata {rows} rows succeed, loadfile: {loadfile} !")
        return rows, action, result
