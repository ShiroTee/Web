#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 11:19
# @Author  : qidl
# @Software: PyCharm

from sqlalchemy import Column, Numeric, Table
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Tuserrole():

    __tablename__ = 'tuserrole'


    l_id = db.Column(db.Numeric(8, 0, asdecimal=False), primary_key=True)
    l_user_id = db.Column(db.Numeric(8, 0, asdecimal=False)),
    l_role_id = db.Column(db.Numeric(8, 0, asdecimal=False))

