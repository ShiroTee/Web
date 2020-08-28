#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/17 17:48
# @Author  : qidl
# @Software: PyCharm
# @Purpose :

import os
import pymssql as ms
import configparser

def msdbConn(node):

    proDir = os.path.split(os.path.realpath(__file__))[0]
    configPath = os.path.join(proDir, "..\..\db.ini")
    path = os.path.abspath(configPath)
    conf = configparser.ConfigParser()
    conf.read(path, encoding='UTF-8')

    dbstr = conf.get(node, "msdb_host")
    user = conf.get(node, "msdb_user")
    pwd = conf.get(node, "msdb_pwd")
    db = conf.get(node, "msdb_db")

    connect = ms.connect(dbstr, user, pwd, db) #服务器名,账户,密码,数据库名
    if connect:
        print("MSDB连接成功!")
    return connect


