#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/22 18:17
# @Author  : qidl
# @Software: PyCharm
# @Description : 封装Redis类

import pickle
import redis

from flask import current_app as app

class Redis(object):

    @staticmethod
    def _getRedis():
        host = app.config['REDIS_HOST']
        port = app.config['REDIS_PORT']
        db = app.config['REDIS_DB']
        passwd = app.config['REDIS_PW']
        r = redis.StrictRedis(host= host, port= port, db= db, password= passwd)

        return r

    @classmethod
    def write(self, key, value, expire=None):
        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = app.config['REDIS_EXPIRE']
        r = self._getRedis()
        r.set(key, value, ex=expire_in_seconds)

    @classmethod
    def write_dict(self, key, value, expire=None):
        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = app.config['REDIS_EXPIRE']
        r = self._getRedis()
        r.set(pickle.dumps(key), pickle.dumps(value), ex=expire_in_seconds)

    @classmethod
    def read_dict(self, key):
        r = self._getRedis()
        data = r.get(pickle.dumps(key))
        if data is None:
            return None
        return pickle.loads(data)

    @classmethod
    def read(self, key):
        r = self._getRedis()
        value = r.get(key)

        return value.decode('utf-8') if value else value

    #写入hash表
    @classmethod
    def hset(self, name, key, value):
        r = self._getRedis()
        r.hset(name, key, value)

    #读取指定hash表的所有给定字段的值
    @classmethod
    def hmset(self, key, *value):
        r = self._getRedis()
        value = r.hmset(key, *value)
        return value

    #读取指定hash表的键值
    @classmethod
    def hget(self, name, key):
        r = self._getRedis()
        value = r.hget(name, key)
        return value.decode('utf-8') if value else value

    #获取指定hash表所有的值
    @classmethod
    def hgetall(self, name):
        r = self._getRedis()
        return r.hgetall(name)

    #删除一个或者多个
    @classmethod
    def delete(self, *names):
        r = self._getRedis()
        r.delete(*names)

    #删除指定hash表的键值
    @classmethod
    def hdel(self, name, key):
        r = self._getRedis()
        r.hdel(name, key)

    @classmethod
    def expire(self, name, expire=None):
        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = app.config['REDIS_EXPIRE']
        r = self._getRedis()
        r.expire(name, expire_in_seconds)

