#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/26 13:54
# @Author  : qidl
# @Software: PyCharm

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # os.environ.get('SECRET_KEY') or 'ciccfund-risk'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CICCFUND_RISK'
    EXPIRES_IN = 9999

    # 系统参数
    HOST = '127.0.0.1'
    PORT = 5050

    # 日志
    LOG_LEVEL = "DEBUG"
    LOG_DIR_NAME = "logs"

    # 数据库公用配置
    # 无警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


    # 发邮件 配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_SUPPRESS_SEND = False
    MAIL_PORT = 465
    MAIL_USE_TLS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # Oracle 配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'oracle+cx_oracle://risk_test:risk_test@172.16.120.85:1521/test'
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 5

    # SQLALCHEMY_BINDS = {
    #     'MINI_CORE' : 'mssql+pymssalq://kettle:Password@mainsql.ciccfund.com:1433/mini_core'
    # }

    # Redis 配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6677
    REDIS_PW = ''
    REDIS_DB = ''
    REDIS_EXPIRE = 60000


    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    PRODUCTION = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}