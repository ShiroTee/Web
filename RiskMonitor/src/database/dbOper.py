#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/28 14:07
# @Author  : qidl
# @Software: PyCharm

from sqlalchemy import create_engine
import cx_Oracle
import pandas as pd
import json


class DBOper:

    '''初始化'''
    def __init__(self, user, password, ip, port, service_name):
        '''初始化参数'''
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port
        self.service_name = service_name

        self.conn = None
        self.db = None
        self.cur = None

    def check_version(self):
        '''查看oracle版本'''
        print(cx_Oracle.clientversion())

    def connect(self):
        '''链接请求'''
        try:
            self.db = cx_Oracle.connect(str(self.user) + '/' + str(self.password) + '@' + str(self.ip) + ':' +
                                        str(self.port) + '/' + str(self.service_name))
            self.db.autocommit = False
            self.cur = self.db.cursor()
            return True
        except:
            print("can't connect database!")
            return False

    def close_connect(self):
        '''关闭光标及数据库链接'''
        self.cur.close()
        self.db.close()

    def go_sql(self, sql):
        '''SQL部分'''
        self.sql = sql
        return self.sql

    def execute(self):
        try:
            self.cur.execute(self.sql)
            return True
        except Exception as e:
            print(e)
            return False

    def read_data(self, size=0):
        '''触发输出结果'''
        data_list = ''
        if self.connect():
            if self.execute():
                if size:
                    data_list = self.cur.fetchmany(size)
                else:
                    data_list = self.cur.fetchall()
                return data_list
                self.close_connect()
        else:
            return False
            self.close_connect()


class data_toDF(DBOper):

    def __init__(self, user, password, ip, port, service_name):
        super().__init__(user, password, ip, port, service_name)

    def read_data(self, size=0):

        if self.connect():
            if self.execute():
                '''输出格式定义'''
                if size:
                    data_list = self.cur.fetchmany(size)
                else:
                    data_list = self.cur.fetchall()

                columns = [i[0].lower() for i in self.cur.description]
                df = pd.DataFrame(data_list, columns=columns)
                return df
                self.close_connect()
        else:
            return False
            self.close_connect()


class data_tolist(DBOper):

    def __init__(self, user, password, ip, port, service_name):
        super().__init__(user, password, ip, port, service_name)

    def lists(self, data):
        '''转二维数组'''
        b = list(data)
        for c in b:
            b[b.index(c)] = list(c)
        return b

    # def lists(self,data) :
    # 	self.b = list(data)
    # 	for self.c in self.b:
    # 		self.b[self.b.index(self.c)] = list(self.c)
    # 	return self.b

    def read_data(self, size=0):
        dl = []
        if self.connect():
            if self.execute():
                '''输出格式定义'''
                if size:
                    data_list = self.cur.fetchmany(size)
                else:
                    data_list = self.cur.fetchall()

                dl = self.lists(data_list)

                return dl
                self.close_connect()
        else:
            return False
            self.close_connect()


class data_toJson(DBOper):

    def __init__(self, user, password, ip, port, service_name):
        super().__init__(user, password, ip, port, service_name)

    def read_data(self, size=0):

        if self.connect():
            if self.execute():
                '''输出格式定义'''
                if size:
                    data_list = self.cur.fetchmany(size)
                else:
                    data_list = self.cur.fetchall()

                col_name = self.cur.description

                list = []

                for row in data_list:
                    dict = {}
                    for col in range(len(col_name)):
                        key = col_name[col][0]
                        value = row[col]
                        dict[key] = value
                    list.append(dict)

                js = json.dumps(list, ensure_ascii=False, indent=2, separators=(',', ':'))
                return js

                self.close_connect()
        else:
            return False
            self.close_connect()