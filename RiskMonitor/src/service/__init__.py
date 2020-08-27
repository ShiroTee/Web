#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/23 17:50
# @Author  : qidl
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask import Blueprint, jsonify, request, current_app as app
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models.users import Tuser
from src.models.role import Trole
from src.models.menu import Tmenu
from src.models.userrole import Tuserrole
from src.models.rolemenu import Trolemenu
from utils.common import *
from utils.code_enum import Code
from utils.redisUtils import Redis
from sqlalchemy import text
from sqlalchemy.sql import func
import datetime
from flask_sqlalchemy import SQLAlchemy
import json
db = SQLAlchemy()


def create_md5(passwd):
    # 创建MD5对象
    m5 = hashlib.md5()
    b = passwd.encode(encoding='utf-8')
    m5.update(b)
    str_md5 = m5.hexdigest()

    return str_md5

def role_constructMenuTree(parentId=0, userId=None):
    if userId:
        menuDate = Tmenu.query.join(Trolemenu, Tmenu.l_menu_id == Trolemenu.l_menu_id).join(Tuserrole, Tuserrole.l_role_id == Trolemenu.l_role_id).filter(
            Tuserrole.l_user_id == userId
        ).filter(Tmenu.l_parent_id == parentId).order_by('l_order').all()
    else:
        menuDate = Tmenu.query.filter(Tmenu.l_parent_id == parentId).order_by(text('l_parent_id, l_order')).all()

    menu_dict = role_menu_to_dict_josn(menuDate)

    if len(menu_dict) > 0:
        data = []
        for menu in menu_dict:
            menu['children'] = role_constructMenuTree(menu['id'], userId)
            data.append(menu)
        return data
    return []

def role_menu_to_dict_josn(data):
    result = []
    for menu in data:
        child = {
            'id': menu.l_menu_id,
            "title": menu.vc_menu_name,
            "spread": True,
        }
        result.append(child)
    return result

def role_update(lst, role_id):
    if lst == []:
       return

    for item in lst:
        id = db.session.query(func.max(Trolemenu.l_id)).scalar()
        newrolemenu = Trolemenu(l_id=id + 1,
                            l_role_id = role_id,
                            l_menu_id = item['id'])
        db.session.add(newrolemenu)
        db.session.commit()
        role_update(item['children'], role_id)


