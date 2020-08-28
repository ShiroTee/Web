#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/7 14:20
# @Author  : qidl
# @Software: PyCharm
# @Purpose : 角色处理主服务

from src.service import *


role = Blueprint('role', __name__)


# 获取角色
@role.route('/index', methods=["POST", "GET"])
def index():
    return render_template('role/role.html', current_user=current_user)
    '''
    req_dir = request.get_json()
    if req_dir is None:
        return NO_PARAMETER()
    role_name = req_dir.get("role_name")
    page = req_dir.get("page")
    page_size = req_dir.get("page_size")
    status = req_dir.get("status")
    order_column_name = req_dir.get("order_column_name")
    order_type = req_dir.get("order_type")
    try:
        model = Trole.query
        if role_name:
            model = model.filter(Trole.vc_role_name.like("%" + role_name + "%"))
        if status is not None:
            model = model.filter(Trole.c_status.in_((1, 2))) if status == 0 else model.filter(Trole.c_status == status)
        if order_column_name and order_type and order_type.lower() in ['asc', 'desc']:
            model = model.order_by(text(f"{order_column_name} {order_type}"))
        if not page or page <= 0:
            page = 1
        if not page_size or page_size <= 0:
            page_size = 10
        result = model.order_by("vc_create_time").paginate(page, page_size, error_out=False)
        data = construct_page_data(result)
        return SUCCESS(data=data)
    except Exception as e:
        app.logger.error(f"获取角色信息失败：{e}")
        return REQUEST_ERROR()
    '''

# 获取角色
@role.route('/getindex', methods=["POST", "GET"])
def getindex():
    try:
        data = []
        roles = Trole.query.all()

        for role in roles:
            role_dict = role.__dict__
            status = role_dict['c_status']
            if status == '0':
                role_dict['c_status'] = '正常'
            elif status == '1':
                role_dict['c_status'] = '注销'
            del role_dict['_sa_instance_state']
            data.append(role_dict)

        return SUCCESS(data=data)
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
        # result = model.paginate(5, 10, error_out=False)
        # data = construct_page_data(result)
        # return SUCCESS(data= data)

    except Exception as e:
        app.logger.error(f"获取用户信息失败：{e}")
        return REQUEST_ERROR()

# 创建新角色
@role.route('/role-add', methods=['POST', 'GET'])
def roleaddpage():
    return render_template('role/role-add.html', current_user=current_user)

# 创建新角色
@role.route('/insert', methods=['POST', 'GET'])
def insertrole():
    role_name = request.values.get('role_name', 0)
    status = 0
    create_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")

    role_id = db.session.query(func.max(Trole.l_role_id)).scalar()
    order = db.session.query(func.max(Trole.l_order)).scalar()

    newrole = Trole(l_role_id=role_id + 1,
                    vc_role_name=role_name,
                    l_order=order + 1,
                    c_status=status,
                    vc_create_time=create_time)
    db.session.add(newrole)
    db.session.commit()
    return SUCCESS(data=[])

# 编辑角色
@role.route('/role-edit', methods=['POST', 'GET'])
def roleupdatepage():
    return render_template('role/role-edit.html', current_user=current_user)

# 构建权限树
@role.route('/tree', methods=['POST', 'GET'])
def constructtree():
    '''
    Redis.delete("rolemenu")
    Redis.delete("rolemenus")
    menu_redis = Redis.read_dict("rolemenu")
    if menu_redis:
        data = menu_redis
        print(data)
        size = len(data)
    else:
    '''
    data = role_constructMenuTree()
    size = len(data)
        #Redis.write_dict("rolemenu", data, 36000)
    return jsonify(code=Code.SUCCESS.value, msg="OK", data=data, length=size)

# 初始化权限树
@role.route('/initialize', methods=['POST', 'GET'])
def initializerole():
    role_id = request.values.get('role_id', 0)

    rolemenus = Trolemenu.query.filter_by(l_role_id=role_id)
    data = []
    id_dic = {}
    id_lst = []

    for rolemenu in rolemenus:
        rolemenu_dict = rolemenu.__dict__
        menus = Tmenu.query.filter_by(l_parent_id=rolemenu_dict['l_menu_id'])
        flag = True
        for menu in menus:
            if menu.__dict__:
                flag = False
                break
        if flag:
            id_lst.append(rolemenu_dict['l_menu_id'])
    id_dic['menu_id'] = id_lst
    data.append(id_dic)
    size = len(data)
    return jsonify(code=Code.SUCCESS.value, msg="OK", data=data, length=size)

# 更新权限树
@role.route('/update', methods=['POST', 'GET'])
def updaterole():
    checkData = json.loads(request.values.get('checkData'))
    role_id = request.values.get('role_id', 0)

    # 先删除
    db.session.query(Trolemenu).filter_by(l_role_id=role_id).delete()
    db.session.commit()

    # 再插入
    role_update(checkData, role_id)

    return SUCCESS(data=[])


# 逻辑删除: C_STATUS=1
@role.route('/delete', methods=['POST', 'PUT'])
def deleterole():
    role_id = request.values.get('role_id', 0)
    #cancel_date = datetime.datetime.now().strftime("%Y%m%d")
    db.session.query(Trole).filter(Trole.l_role_id == role_id).update({"c_status": 1})
    db.session.commit()

    return SUCCESS(data=[])

'''
# 更新角色
@role.route('/update', methods=["POST", "PUT"])
def role_update():

    req_dir = request.get_json()
    if req_dir is None:
        return NO_PARAMETER()
    if request.method == "POST":
        id = req_dir.get("id")
        if id:
            model = Trole.query.get(id)
            if model:
                dict_data = model_to_dict(model)
                #获取菜单列表和部门列表
                role_menu = Trolemenu.query.with_entities(Trolemenu.l_menu_id).filter(Trolemenu.l_role_id == id).order_by("l_menu_id").all()
                menu_list = [str(i[0]) for i in role_menu]
                dict_data['role_menu'] = ','.join(menu_list)
                return SUCCESS(dict_data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        id = req_dir.get("id")
        role_name = req_dir.get("role_name")
        role_order = req_dir.get("role_order")
        remark = req_dir.get("remark")
        status = req_dir.get("status")
        role_menu = req_dir.get("role_menu")

        if id and role_name:
            model = Trole.query.get(id)
            if model:
                try:
                    token = request.headers["Authorization"]
                    user = verify_token(token)
                    model.vc_role_name = role_name
                    model.c_status = status
                    model.vc_remark = remark
                    model.vc_update_user = user['name']
                    model.update()
                    try:
                        #更新菜单列表
                        update_menu(id, role_menu)
                        return SUCCESS()
                    except Exception as e:
                        app.logger.error(f"更新菜单失败:{e}")
                        return UPDATE_ERROR(msg="更新菜单失败")
                except Exception as e:
                    app.logger.error(f"更新角色失败:{e}")
                    return UPDATE_ERROR()

            else:
                return ID_NOT_FOUND()
        else:
            return NO_PARAMETER()


# 创建角色 TODO
@role.route('/create', methods=["PUT"])
def create():
    req_dir = request.get_json()
    if req_dir is None:
        return NO_PARAMETER()
    role_name = req_dir.get("role_name")
    role_order = req_dir.get("role_order")
    remark = req_dir.get("remark")
    status = req_dir.get("status")
    role_menu = req_dir.get("role_menu")
    token = request.headers["Authorization"]
    user = verify_token(token)
    if role_name:
        try:
            is_exist = Trole.query.filter(Trole.vc_role_name == role_name).first()
            if is_exist:
                return CREATE_ERROR(msg="角色名称已存在")
            model = Trole()
            model.vc_role_name = role_name
            model.role_order = role_order
            model.vc_remark = remark
            model.c_status = status
            model.vc_create_user = user['name']
            model.save()
            if role_menu:
                try:
                    # 向角色菜单表插入数据
                    role_id = model.l_role_id
                    menu_list = role_menu.split(',')
                    insert_list = []
                    for menu_id in menu_list:
                        insert_list.append({"role_id": role_id, "menu_id": menu_id})
                    if len(insert_list) > 0:
                        role_menu_model = Trolemenu()
                        role_menu_model.save_all(insert_list)
                    return SUCCESS()
                except Exception as e:
                    model.delete()
                    app.logger.error(f"新建角色失败:{e}")
                    return CREATE_ERROR()
            else:
                return SUCCESS()
        except Exception as e:
            app.logger.error(f"新建角色失败:{e}")
            return CREATE_ERROR()
    else:
        return NO_PARAMETER()

# 根据ID删除角色 TODO
@role.route('/delete', methods=["DELETE"])
def delete():
    req_dir = request.get_json()
    if req_dir is None:
        return NO_PARAMETER()
    role_id = req_dir.get("id")
    if role_id:
        try:
            role = Trole.query.get(role_id)
            if role_id:
                # user_role = User_Role.query.filter_by(role_id=role_id).all()
                # if user_role:
                #     return DELETE_ERROR(msg="该角色已关联用户，无法删除！")

                role_menu = Trolemenu.query.filter_by(role_id=role_id).all()
                if role_menu:
                    for menu in role_menu:
                        menu.delete()
                role.delete()
                return SUCCESS()
            else:
                return ID_NOT_FOUND()
        except Exception as e:
            app.logger.error(f"删除角色失败:{e}")
            return DELETE_ERROR()
    else:
        return PARAMETER_ERR()


# 更新菜单  TODO
def update_menu(id, role_menu):
    menu_db = Trolemenu.query.filter(
        Trolemenu.l_role_id == id).all()
    if role_menu:  # 如果有菜单
        # 获取数据库菜单列表
        db_list = [str(i.menu_id) for i in menu_db]
        # 获取传过来的参数
        par_list = role_menu.split(',')
        # 获取需要删除和增加的数据
        add_list, less_list = get_diff(db_list, par_list)
        if len(less_list) > 0:
            # 删除没有权限的菜单
            for menu in menu_db:
                if str(menu.menu_id) in less_list:
                    menu.delete()
        if len(add_list) > 0:
            insert_list = []
            for menu_id in add_list:
                insert_list.append({"role_id": id, "menu_id": menu_id})
            role_menu_model = Trolemenu()
            role_menu_model.save_all(insert_list)
    else:  # 如果没菜单
        # 获取数据库菜单列表
        for menu in menu_db:
            menu.delete()
'''
