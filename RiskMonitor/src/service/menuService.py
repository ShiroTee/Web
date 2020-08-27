#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 17:40
# @Author  : qidl
# @Software: PyCharm
# @Purpose : 菜单处理主服务

from src.service import *

menu = Blueprint('menu', __name__)

#获取用户菜单
@menu.route('/search', methods=['POST'])
@login_required
def search_user_menu():
    req_dir = request.get_json()
    user_id = req_dir.get('userId')

    # 获取菜单树
    data = constructMenuTree(userId= user_id)

    return jsonify(code=Code.SUCCESS.value, msg="OK", data=data)

# 获取菜单信息
@menu.route('/menus', methods=['GET','POST'])
def query_menus():
    # req_dir = request.get_json()
    # if req_dir is None:
    #     return NO_PARAMETER()

    # 返回所有数据
    Redis.delete("menu")
    Redis.delete("menus")
    menu_redis = Redis.read_dict("menu")
    if menu_redis:
        data = menu_redis
        size = len(data)
    else:
        data = constructMenuTree()
        size = len(data)
        Redis.write_dict("menu", data, 36000)
    return jsonify(code=Code.SUCCESS.value, msg="OK", data=data, length=size, )

# 添加菜单
# TODO
@menu.route('/insert', methods=['PUT'])
def insert_menu():
    pass

# 删除菜单
# TODO
@menu.route('/delete', methods=['DELETE'])
def delete_menu():
    pass

# 更新菜单信息
# TODO
@menu.route('/update', methods=['POST', 'PUT'])
def update_menu():
    pass




# 通过递归实现根据父ID查找子菜单,如果传入用户id则只查询该用户的权限否则查询所有权限,一级菜单父id默认是0
    ''' 
    1.根据父ID获取该菜单下的子菜单或权限
    2.遍历子菜单或权限，继续向下获取，直到最小级菜单或权限
    3.如果没有遍历到，返回空的数组，有返回权限列表 
    '''
def constructMenuTree(parentId=0, userId=None):
    if userId:
        menuDate = Tmenu.query.join(Trolemenu, Tmenu.l_menu_id == Trolemenu.l_menu_id).join(Tuserrole, Tuserrole.l_role_id == Trolemenu.l_role_id).filter(
            Tuserrole.l_user_id == userId
        ).filter(Tmenu.l_parent_id == parentId).order_by('l_order').all()
    else:
        menuDate = Tmenu.query.filter(Tmenu.l_parent_id == parentId).order_by(text('l_parent_id, l_order')).all()

    menu_dict = menu_to_dict_josn(menuDate)

    if len(menu_dict) > 0:
        data = []
        for menu in menu_dict:
            menu['children'] = constructMenuTree(menu['menu_id'], userId)
            data.append(menu)
        return data
    return []
#
#
# # 格式化菜单字段显示顺序
# def menu_to_dict(data):
#     result = []
#     for menu in data:
#         child = {
#             "menu_id": menu.l_menu_id,
#             "menu_name": menu.vc_menu_name,
#             "parent_id": menu.l_parent_id,
#             "order_num": menu.l_order,
#             "url": menu.vc_url,
#             "menu_type": menu.vc_menu_type,
#             "create_user": menu.vc_create_user,
#             "created_time": menu.vc_create_time,
#             "update_by": menu.vc_update_user,
#             "updated_at": menu.vc_update_time,
#             "remark": menu.vc_remark,
#         }
#         result.append(child)
#     return result

# 格式化菜单字段显示顺序(左侧菜单栏)
def menu_to_dict_josn(data):
    result = []
    for menu in data:
        child = {
            "menu_id": menu.l_menu_id,
            "title": menu.vc_menu_name,
            "parent_id": menu.l_parent_id,
            "order_num": menu.l_order,
            "path": menu.vc_url,
            "menu_type": menu.vc_menu_type,
            "icon": menu.vc_icon,
            "spread": menu.c_spread,
        }
        result.append(child)
    return result
