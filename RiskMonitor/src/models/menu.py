# coding: utf-8
from sqlalchemy import Column, Numeric, String
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Tmenu(db.Model):
    __tablename__ = 'tmenu'

    l_menu_id = db.Column(db.Numeric(8, 0, asdecimal=False), primary_key=True, info='菜单ID')
    vc_menu_name = db.Column(db.String(50), nullable=False, info='菜单名')
    l_parent_id = db.Column(db.Numeric(8, 0, asdecimal=False), info='父菜单ID')
    l_order = db.Column(db.Numeric(4, 0, asdecimal=False), info='顺序')
    vc_url = db.Column(db.String(200), info='URL')
    vc_menu_type = db.Column(db.String(1), info='菜单类型 1：目录；2：菜单；3：按钮')
    vc_create_user = db.Column(db.String(50))
    vc_create_time = db.Column(db.String(20))
    vc_update_user = db.Column(db.String(50))
    vc_update_time = db.Column(db.String(20))
    vc_remark = db.Column(db.String(100), info='备注')
    vc_icon = db.Column(db.String(20))
    c_spread = db.Column(db.String(1))
