#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/23 17:50
# @Author  : qidl
# @Software: PyCharm
# @Purpose : 用户处理主服务


from src.service import *

user = Blueprint('user', __name__)

class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired()])
    password = StringField(u'密  码', validators=[DataRequired()])
    rememberme = BooleanField(label=u'记住我', default=False)
    submit = SubmitField(u'登  录')

# 用户登录
@user.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form.get("username")
        password = request.form.get("password")
        #校验参数
        #if not all([username, password]):
        #    return jsonify(code = Code.NOT_NULL.value, msg = "登录账号和密码不能为空")
        try:
            user = Tuser.query.filter_by(vc_login_id= username).first()

        except Exception as e:
            app.logger.error("login error : {}".format(e))
            return jsonify(code=Code.ERR_PWD.value, msg = "数据库错误")

        if user is None or not user.verify_password(password) or user.c_status == 2:
            #return jsonify(code= Code.ERR_PWD.value, msg= "登录账号或密码错误")
            flash({'error': u'登录账号或密码错误！'})
            return render_template('login.html', form=form)

        # TODO获取用户角色
        # user_role = Role.query.join(User_Role, Role.id == User_Role.role_id).join(User,User_Role.user_id == user.id).filter(User.id == user.id).all()
        # userRole = Trole.query.join(Tuserrole, Trole.l_role_id == Tuserrole.l_role_id).filter(Tuserrole.l_user_id == user.l_user_id).all()
        # role_list = [i.l_role_id for i in userRole]
        # token = create_token(user.l_user_id, user.vc_user_name, role_list)
        token = create_token(user.l_user_id, user.vc_user_name, user.c_status)

        data = {'token': token,
                'userId': user.l_user_id,
                'loginID': user.vc_login_id,
                'userName': user.vc_user_name}

        try:
            # 写入缓存
            Redis.write(f"token_{user.vc_login_id}", token)

        except Exception as e:
            #return jsonify(code= Code.UPDATE_DB_ERROR.value, msg="登录失败")
            flash({'error': u'登录失败！'})

        if token:
            #return jsonify(code= Code.SUCCESS.value, msg="登录成功", data= data)
            #return render_template('index.html', form=form)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            #return jsonify(code=Code.REQUEST_ERROR.value, msg="登录失败", data=data)
            return render_template('login.html', form=form, msg="登录失败", data=token)

    return render_template('login.html', form= form)

@user.route('/logout', methods= ['GET', 'POST'])
#@login_required()
def logout():
    form = LoginForm(request.form)
    try:
        token = request.headers["Authorization"]
        user = verify_token(token)
        if user:
            key = f"token_{user.get('name')}"
            redis_token = Redis.read(key)
            if redis_token:
                Redis.delete(key)
            #return SUCCESS()
            return render_template('login.html', form=form)
        else:
            return AUTH_ERR()
    except Exception as e:
        app.logger.error(f"注销失败")
        return REQUEST_ERROR()


@user.route('/check_token', methods=['POST'])
def check_token():
    token = request.headers["Authorization"]
    user = verify_token(token)
    if user:
        key = f"token_{user.get('name')}"
        redis_token = Redis.read(key)
        if redis_token == token:
            return SUCCESS(data=user.get('id'))
        else:
            return OTHER_LOGIN()
    else:
        return AUTH_ERR()

# 获取所有用户信息
@user.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('user/user.html', current_user=current_user)


@user.route('/getindex', methods=['POST', 'GET'])
def getindex():
    # req_dir = request.get_json()
    # if req_dir is None:
    #     return NO_PARAMETER()

    # userName = req_dir.get("user_name")
    # phone = req_dir.get("phone")
    # order_column_name = req_dir.get("order_column_name")
    # order_type = req_dir.get("order_type")
    # page = req_dir.get("page")
    # pageSize = req_dir.get("page_size")
    # status = req_dir.get("status")

    try:
        status = request.values.get('c_status', -1)
        data = []
        if status == -1:
            users = Tuser.query.all()
        else:
            users = Tuser.query.filter_by(c_status=status)

        for user in users:
            user_dict = user.__dict__
            status = user_dict['c_status']
            if status == '0':
                user_dict['c_status'] = '正常'
            elif status == '1':
                user_dict['c_status'] = '冻结'
            elif status == '2':
                user_dict['c_status'] = '注销'
            del user_dict['_sa_instance_state']
            data.append(user_dict)
        return SUCCESS(data= data)
        # model = Tuser.query.filter(Tuser.c_status == '0')
        # if userName :
        #     model = model.filter(Tuser.vc_user_name.like("%" + userName + "%"))
        # if phone:
        #     model = model.filter(Tuser.vc_phone.like("%" + phone + "%"))
        # if status is not None:
        #     model = model.filter(Tuser.c_status.in_(0, 1))
        # if order_column_name and order_type and order_type.lower() in ['asc', 'desc']:
        #     model.order_by(text(f"{order_column_name} {order_type}"))
        # if not page or page <= 0:
        #     page = 1
        # if not pageSize or pageSize <= 0:
        #     pageSize = 10
        #result = model.paginate(5, 10, error_out=False)
        #data = construct_page_data(result)
        #return SUCCESS(data= data)

    except Exception as e:
        app.logger.error(f"获取用户信息失败：{e}")
        return REQUEST_ERROR()


@user.route('/search', methods=['POST', 'PUT'])
def searchdata():
    username = request.values.get('username', 0)
    user = Tuser.query.filter_by(vc_login_id=username).first()
    if user is not None:
        data = []
        user_dict = user.__dict__
        status = user_dict['c_status']
        if status == '0':
            user_dict['c_status'] = '正常'
        elif status == '1':
            user_dict['c_status'] = '冻结'
        elif status == '2':
            user_dict['c_status'] = '注销'
        del user_dict['_sa_instance_state']
        data.append(user_dict)

        return SUCCESS(data=data)
    else:
        return SUCCESS(data=[])

@user.route('/user-add', methods=['POST', 'GET'])
def useraddpage():
    return render_template('user/user-add.html', current_user=current_user)

@user.route('/insert', methods=['POST', 'PUT'])
def insertdata():
    login_id = request.values.get('login_id', 0)
    user_name = request.values.get('user_name', 0)
    password = request.values.get('password', 0)
    password = create_md5(password)
    emails = request.values.get('emails', 0)
    phone = request.values.get('phone', 0)
    status = request.values.get('status', 0)
    reg_date = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")

    user_id = db.session.query(func.max(Tuser.l_user_id)).scalar()

    newuser = Tuser( l_user_id=user_id+1,
                     vc_login_id=login_id,
                     vc_user_name=user_name,
                     vc_password=password,
                     vc_emails=emails,
                     vc_phone=phone,
                     c_status=status,
                     vc_reg_date=reg_date)

    db.session.add(newuser)
    db.session.commit()

    return SUCCESS(data=[])

@user.route('/user-edit', methods=['POST', 'GET'])
def userupdatepage():
    return render_template('user/user-edit.html', current_user=current_user)

@user.route('/update', methods=['POST', 'PUT'])
def updatedata():
    user_id = request.values.get('user_id', 0)
    login_id = request.values.get('login_id', 0)
    user_name = request.values.get('user_name', 0)
    password = request.values.get('password', 0)
    emails = request.values.get('emails', 0)
    phone = request.values.get('phone', 0)
    status = request.values.get('status', 0)
    print(status)

    db.session.query(Tuser).filter(Tuser.l_user_id == user_id).update({"vc_login_id": login_id,
                                                                       "vc_user_name": user_name,
                                                                       "vc_password": password,
                                                                       "vc_emails": emails,
                                                                       "vc_phone": phone,
                                                                       "c_status": status})

    if status == '0' or status == '1':
        db.session.query(Tuser).filter(Tuser.l_user_id == user_id).update({"vc_cancel_date": ""})
    db.session.commit()
    return SUCCESS(data=[])

# 重设密码页面
@user.route('/user-reset', methods=['POST', 'GET'])
def userresetpage():
    return render_template('user/user-reset.html', current_user=current_user)

# 重设密码
@user.route('/reset', methods=['POST', 'GET'])
def resetpassword():
    user_id = request.values.get('user_id', 0)
    password = request.values.get('password', 0)
    password = create_md5(password)

    db.session.query(Tuser).filter(Tuser.l_user_id == user_id).update({"vc_password": password})
    db.session.commit()
    return SUCCESS(data=[])


# 逻辑删除: C_STATUS=2
@user.route('/delete', methods=['POST', 'PUT'])
def deletedata():
    user_id = request.values.get('user_id', 0)
    cancel_date = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
    db.session.query(Tuser).filter(Tuser.l_user_id == user_id).update({"c_status": 2,
                                                                       "vc_cancel_date":cancel_date})
    db.session.commit()

    return SUCCESS(data=[])











