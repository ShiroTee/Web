# coding: utf-8
from sqlalchemy import Column, Numeric, String
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Trole(db.Model):
    __tablename__ = 'trole'

    l_role_id = db.Column(db.Integer(), primary_key=True)
    vc_role_name = db.Column(db.String(50))
    l_order = db.Column(db.Numeric(4, 0, asdecimal=False))
    c_status = db.Column(db.String(1))
    vc_create_user = db.Column(db.String(50))
    vc_create_time = db.Column(db.String(20))
    vc_update_user = db.Column(db.String(50))
    vc_update_time = db.Column(db.String(20))
    vc_remark = db.Column(db.String(100))
