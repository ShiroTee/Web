#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 11:19
# @Author  : qidl
# @Software: PyCharm

from sqlalchemy import Column, Numeric, Table
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Trolemenu(db.Model):
    __tablename__ = 'trolemenu'
    l_id = db.Column(db.Integer(), primary_key=True)
    l_role_id = db.Column(db.Integer())
    l_menu_id = db.Column(db.Integer())
