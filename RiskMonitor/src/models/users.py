#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 11:19
# @Author  : qidl
# @Software: PyCharm

import hashlib
from src.models import *


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Tuser(db.Model):
    __tablename__ = 'tuser'

    l_user_id = db.Column(db.Integer(), primary_key=True, info='用户ID')
    vc_login_id = db.Column(db.String(30), nullable=False, unique=True, info='登录ID')
    vc_user_name = db.Column(db.String(50), nullable=False, info='用户名')
    vc_password = db.Column(db.String(50), nullable=False, info='密码')
    vc_domain_name = db.Column(db.String(32), info='域用户名')
    vc_emails = db.Column(db.String(50), info='邮箱')
    vc_phone = db.Column(db.String(20), info='电话')
    c_status = db.Column(db.String(1), server_default=db.FetchedValue(), info='状态，0：正常；1：冻结；2：注销')
    vc_reg_date = db.Column(db.String(8), info='注册日期')
    vc_cancel_date = db.Column(db.String(8), info='注销日期')
    l_dept_id = db.Column(db.Numeric(8, 0, asdecimal=False), info='部门ID')
    l_group_id = db.Column(db.Numeric(8, 0, asdecimal=False), info='用户组ID')
    vc_remark = db.Column(db.String(100), info='备注')

    # 验密
    def verify_password(self, passwd):
        # 创建MD5对象
        m5 = hashlib.md5()
        b = passwd.encode(encoding= 'utf-8')
        m5.update(b)
        str_md5 = m5.hexdigest()
        if self.vc_password == str_md5:
            return 1
        else:
            return 0

