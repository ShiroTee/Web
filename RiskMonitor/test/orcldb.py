#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/17 14:14
# @Author  : qidl
# @Software: PyCharm

from flask_sqlalchemy import SQLAlchemy as db
import cx_Oracle as cx
#from src.database.dbOper import DBOper as database



app.config['SQLALCHEMY_DATABASE_URI'] = config[config_name].SQLALCHEMY_DATABASE_URI

conn = cx.connect('risk_test/risk_test@172.16.120.85:1521/test')

#(self, user, password, ip, port, service_name):
#conn = database.__init__('risk_test', 'risk_test', '172.16.120.85', '1521', 'test')


cursor = conn.cursor()

cursor.execute("select * from tuser ")

data = cursor.fetchone()

print(data)

cursor.close()

conn.close()