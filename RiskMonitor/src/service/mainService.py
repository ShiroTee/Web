#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 17:36
# @Author  : qidl
# @Software: PyCharm
# 主页

from src.service import *
from src.database.msdbOper import msdbConn
from flask import render_template, Response, request
import pandas as pd
import json
import datetime

main = Blueprint('main', __name__)


# 根目录跳转
# @main.route('/', methods=['GET', 'POST'])
# @login_required
# def root():
#     return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
#@login_required
def index():
    return render_template('index.html', current_user=current_user)

@main.route('/portfolioReturn', methods=['GET'])
#@login_required
def portfolioPerformance():
    return render_template('portfolioPerformance/portfolioReturn.html', current_user=current_user)

# for test ms sql
@main.route('/perf', methods=['GET'])
def perf():
    data = []

    print('start')
    users = Tuser.query.filter(Tuser.c_status == '0').first()
    for user in users:
        user_dict = user.__dict__
        del user_dict['_sa_instance_state']
        data.append(user_dict)

    print('end')
    print(data)
    sss = {}
    return jsonify(data=data)


# 组合代码下拉框
@main.route('/portfolioReturn/get_code_lst', methods=['GET','POST'])
#@login_required
def get_code_lst():
    conn = msdbConn('msdb')
    sqli = '''SELECT 组合编号 + ' ' + 组合名称 as 组合代码 FROM [MINI_CORE].[CICC_IA].[组合信息表] where 组合编号 like 'Z%' order by 组合编号 asc'''
    portfolio_return_code_df = pd.read_sql(sqli, conn)
    code_lst = list(portfolio_return_code_df['组合代码'])

    res_dict = dict()
    res_dict['data'] = []

    for i in range(len(code_lst)):
        item = dict()
        item['value'] = i
        item['name'] = code_lst[i]
        res_dict['data'].append(item)

    # 传回前端的数据需要json化再转换为Response
    return Response(json.dumps(res_dict, ensure_ascii=False), content_type='application/json')


# 基准下拉框
@main.route('/portfolioReturn/get_index')
def get_index():
    conn = msdbConn('msdb')
    code = request.values.get('code', 0)
    code = code.split()[0]
    end = request.values.get('end', 0)
    sqli1 = '''select 基准模式 FROM [MINI_CORE].[CICC_IA].[组合信息表] where 组合编号 = '%s'    ''' % (code)

    index_df = pd.read_sql(sqli1, conn)
    index_lst = list(index_df['基准模式'])[0].split('/')
    if '' in index_lst:
        index_lst.remove('')

    sqli2 = ''' SELECT 基准编号,名称,基准用途 FROM [MINI_CORE].[CICC_IA].[业绩基准表] where 起始日期 <= '%s' and isnull(截止日期, '99991231') > '%s' ''' %(end, end)
    index_name = pd.read_sql(sqli2, conn)

    res_lst = []
    for i in index_lst:
        res_lst.append(index_name[index_name['基准编号'] == i].values.tolist()[0])

    for i in range(len(res_lst)):
        res_lst[i] = res_lst[i][0] + '   ' + res_lst[i][1] + ' (' + res_lst[i][2] + ')'


    res_dict = {}
    res_dict['data'] = []
    for i in range(len(res_lst)):
        item = dict()
        item['value'] = i
        item['name'] = res_lst[i]
        res_dict['data'].append(item)


    # 传回前端的数据需要json化再转换为Response
    return Response(json.dumps(res_dict, ensure_ascii=False), content_type='application/json')

# 组合业绩表
@main.route('/portfolioReturn/get_start_end')
def get_start_end():
    conn = msdbConn('msdb')
    # 得到前端传回的参数
    start = request.values.get('start', 0)
    end = request.values.get('end', 0)
    # 数组从前端传回json化, 因此需要json.loads()
    code_name = json.loads(request.values.get('code_lst'))
    code_lst = json.loads(request.values.get('code_lst'))
    for i in range(len(code_lst)):
        code_lst[i] = code_lst[i].split(' ')[0]

    # 将code_lst转化为code_str方便数据库调用
    for i in range(len(code_lst)):
        code_lst[i] = '\'' + code_lst[i] + '\''
    code_str = ','.join(code_lst)
    print(code_str)
    sqli = '''SELECT a.日期, a.组合代码 + ' ' + b.组合名称 as  组合代码, a.组合累计收益率 FROM [MINI_CORE].[IA].[RISK_组合业绩表] a
                 left join [MINI_CORE].[CICC_IA].[组合信息表] b on a.组合代码 = b.组合编号
                where a.组合代码 in (%s) and a.日期 >= '%s' and a.日期 <= '%s' order by a.日期 asc''' % (
        code_str, start, end)
    print(sqli)
    portfolio_return_df = pd.read_sql(sqli, conn)
    code = portfolio_return_df['组合代码'].unique()
    print(portfolio_return_df)
    res_dict = {}
    res_dict['start'] = [start]
    res_dict['end'] = [end]
    res_dict['date'] = list(portfolio_return_df['日期'])

    # 日期转换为 年/月/日
    for i in range(len(res_dict['date'])):
        res_dict['date'][i] = res_dict['date'][i][:4] + '-' + res_dict['date'][i][4:6] + '-' + res_dict['date'][i][6:]

    portfolio_return_df['日期'] = pd.DataFrame(res_dict['date'])

    # 计算区间收益率
    for i in range(len(code)):
        tmp = portfolio_return_df[portfolio_return_df['组合代码'] == code[i]][['日期', '组合累计收益率']].values.tolist()
        if len(tmp) <= 1:
            tmp = []
        else:
            tmp_first = tmp[0][1]
            for j in range(len(tmp)):
                tmp[j][1] = round((1 + tmp[j][1]) / (1 + tmp_first) - 1, 4)

        res_dict[code[i]] = tmp

    # 用输入的起止时间得到X轴坐标
    xlab = []
    cur_date = start
    while cur_date <= end:
        xlab.append(cur_date)
        cur_date = datetime.datetime.strftime(
            datetime.datetime.strptime(cur_date, '%Y-%m-%d') + datetime.timedelta(days=1), '%Y-%m-%d')
    res_dict['xlab'] = xlab

    # 传回前端的数据需要json化再转换为Response
    return Response(json.dumps(res_dict, ensure_ascii=False), content_type='application/json')


# 组合基准对比表
@main.route('/portfolioReturn/get_start_end_index')
def get_start_end_index():
    conn = msdbConn('msdb')

    # 得到前端传回的参数
    start = request.values.get('start', 0)
    end = request.values.get('end', 0)
    code = json.loads(request.values.get('code'))[0]
    code2 = json.loads(request.values.get('code'))[0].split(' ')[0]

    index_lst = json.loads(request.values.get('index_lst'))

    print(code)

    res_dict = {}
    res_dict['start'] = [start]
    res_dict['end'] = [end]

    # 组合
    sqli1 = '''SELECT a.日期, a.组合代码 + ' ' + b.组合名称 as 组合代码, a.组合累计收益率 FROM [MINI_CORE].[IA].[RISK_组合业绩表] a
                 left JOIN [MINI_CORE].[CICC_IA].[组合信息表] b on a.组合代码 = b.组合编号
                where a.组合代码 ='%s' and a.日期 >= '%s' and a.日期 <= '%s' order by a.日期 asc''' % (
        code2, start, end)
    portfolio_return_df = pd.read_sql(sqli1, conn)

    print(portfolio_return_df)
    res_dict['date'] = list(portfolio_return_df['日期'])
    # 日期转换为 年/月/日
    for i in range(len(res_dict['date'])):
        res_dict['date'][i] = res_dict['date'][i][:4] + '-' + res_dict['date'][i][4:6] + '-' + res_dict['date'][i][6:]

    print(123)
    print(res_dict['date'])
    portfolio_return_df['日期'] = pd.DataFrame(res_dict['date'])

    # 计算组合区间收益率
    tmp = portfolio_return_df[['日期', '组合累计收益率']].values.tolist()
    if len(tmp) <= 1:
        tmp = []
    else:
        tmp_first = tmp[0][1]
        for j in range(len(tmp)):
            tmp[j][1] = round((1 + tmp[j][1]) / (1 + tmp_first) - 1, 4)
    res_dict[code] = tmp

    # 基准
    for i in range(len(index_lst)):
        index_lst[i] = '\'' + index_lst[i].split(' ')[0] + '\''
        # 将code_lst转化为code_str方便数据库调用

    index_str = ','.join(index_lst)

    sqli2 = '''SELECT 日期,基准名称,基准代码,基准累计收益率 FROM [MINI_CORE].[IA].[RISK_基准业绩表] 
            where 日期 >= '%s' and 日期 <= '%s' and 基准代码 in (%s) and 组合代码 = '%s' order by 日期 asc''' % (
        start, end, index_str, code2)
    index_return_df = pd.read_sql(sqli2, conn)

    index = index_return_df['基准代码'].unique()
    print(index)
    res_dict['date'] = list(index_return_df['日期'])
    # 日期转换为 年/月/日
    for i in range(len(res_dict['date'])):
        res_dict['date'][i] = res_dict['date'][i][:4] + '-' + res_dict['date'][i][4:6] + '-' + res_dict['date'][i][6:]
    index_return_df['日期'] = pd.DataFrame(res_dict['date'])

    # 计算基准区间收益率
    index2 = json.loads(request.values.get('index_lst'))
    print(index2)
    for i in range(len(index)):
        tmp = index_return_df[index_return_df['基准代码'] == index[i]][['日期', '基准累计收益率']].values.tolist()
        if len(tmp) <= 1:
            tmp = []
        else:
            tmp_first = tmp[0][1]
            for j in range(len(tmp)):
                tmp[j][1] = round((1 + tmp[j][1]) / (1 + tmp_first) - 1, 4)

        for j in index2:
            if index[i] in j:
                res_dict[j] = tmp


    # 用输入的起止时间得到X轴坐标
    xlab = []
    cur_date = start
    while cur_date <= end:
        xlab.append(cur_date)
        cur_date = datetime.datetime.strftime(
            datetime.datetime.strptime(cur_date, '%Y-%m-%d') + datetime.timedelta(days=1), '%Y-%m-%d')
    res_dict['xlab'] = xlab

    # 传回前端的数据需要json化再转换为Response
    return Response(json.dumps(res_dict, ensure_ascii=False), content_type='application/json')
