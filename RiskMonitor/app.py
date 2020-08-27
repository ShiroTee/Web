#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/26 13:54
# @Author  : qidl
# @Software: PyCharm
# @Des: 初始化app

from flask import Flask
from flask_cors import CORS
from utils.logutil import handler
from config import config
from flask_login import LoginManager
from src.service import userService
from src.service import mainService
from src.service import roleService
from src.service import menuService
#from src.database.dbOper import DBOper as database
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

loginManager = LoginManager()
loginManager.session_protection = 'strong'
loginManager.login_view = 'login'

@loginManager.user_loader
def load_user(user_id):
    #return Tuser.get(Tuser.l_user_id == int(user_id))
    return None

def create_app(config_name):
    app = Flask(__name__, template_folder='templates', static_folder='static',static_url_path='/static')

    # 加载配置文件
    app.config.from_object(config[config_name])

    app.config['JSON_AS_ASCII'] = False

    # 配置跨域
    # CORS(app, resources={r"/risk/*":{"origins" : "*"}})

    # 加载日志配置
    app.logger.addHandler(handler)

    # 加载数据库
    init_db(app, config_name)

    # 注册蓝图
    register_blueprints(app)

    loginManager.init_app(app)

    # 加载Redis
    init_redis(app, config_name)



    config[config_name].init_app(app)
    return app


#加载数据库
def init_db(app, config_name):
    # 连接主库
    app.config['SQLALCHEMY_DATABASE_URI'] = config[config_name].SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    # app.config['SQLALCHEMY_BINDS'] = config[config_name].SQLALCHEMY_BINDS

    db.init_app(app)


#加载Redis
def init_redis(app, config_name):
    app.config['REDIS_HOST'] = config[config_name].REDIS_HOST
    app.config['REDIS_PORT'] = config[config_name].REDIS_PORT
    app.config['REDIS_DB'] = config[config_name].REDIS_DB
    app.config['REDIS_PWD'] = config[config_name].REDIS_PW
    app.config['REDIS_EXPIRE'] = config[config_name].REDIS_EXPIRE

#创建蓝图
def register_blueprints(app):
    app.register_blueprint(userService.user, url_prefix='/risk/user')
    app.register_blueprint(roleService.role, url_prefix='/risk/role')
    app.register_blueprint(menuService.menu, url_prefix='/risk/menu')
    app.register_blueprint(mainService.main, url_prefix='/risk/main')



