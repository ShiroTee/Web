#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/17 15:00
# @Author  : qidl
# @Software: PyCharm

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class BaseModel(db.Model):
    ## 声明当前类为抽象类，被继承，调用不会被创建
    __abstract__ = True
    l_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vc_create_user = db.Column(db.String(50), comment="创建人")
    vc_create_time = db.Column(db.String(20), comment="创建时间", server_default=func.now())
    vc_update_user = db.Column(db.String(50), comment="更新人")
    vc_update_time = db.Column(db.String(20), comment="更新时间", server_default=func.now())
    vc_remark = db.Column(db.String(100), comment="备注")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.merge(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert_all(self, data):
        db.session.execute(
            self.__table__.insert(),
            data
        )
        db.session.commit()

