#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/23 10:41
# @Author  : qidl
# @Software: PyCharm

from config import config
from flask import Flask, current_app
from utils.redisUtils import Redis

app = Flask(__name__)

app.config.from_object(config)
with app.app_context():
    pass

app.app_context().push()

#bp = Blueprint(service_name, __name__, url_prefix="/")

#r.write(key='risk', value= 'ciccfund')

#print(r.read(key='risk'))


#host = app.config.SECRET_KEY
#host = app.config #['SECRET_KEY']

host = app.config['default'].REDIS_HOST
print(host)


#@bp.route('/testRedisWrite', methods=['GET'])
def test_redis_write():
    """
    测试redis
    """
    Redis.write("test_key","test_value",60)
    return "ok"

#@bp.route('/testRedisRead', methods=['GET'])
def test_redis_read():
    """
    测试redis
    """
    data = Redis.read("test_key")
    return data


test_redis_write()

data = test_redis_read()
print(data)