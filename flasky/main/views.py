from flask import render_template
from main import main
import pymssql as ms
from config import DB
from flask import render_template, Response, request
import json
import pandas as pd
import datetime
import re


# 1. 创建连接
conn = ms.connect(DB.HOST, DB.USER, DB.PASSWD, DB.DBNAME)
cur = conn.cursor()

@main.route('/correct/YYRating', methods=['GET','POST'])
def code_lst_inteval():

    sqli = '''SELECT TOP 1000 * FROM [riskgroup].[IA].[bond_trans_YYRating] '''
    YYRating_df = pd.read_sql(sqli, conn)
    YYRating_json = json.loads(YYRating_df.to_json(orient='index', force_ascii=False))
    data = []
    count = 0
    for i in YYRating_json.keys():
        data.append(YYRating_json[i])
        count += 1

    res_dict = {"code":0,
                "msg":"",
                "count":count,
                "data":data
                }
    # 传回前端的数据需要json化再转换为Response
    return Response(json.dumps(res_dict, ensure_ascii=False), content_type='application/json')

@main.route('/correct/graph1/get_start_end_index')
def get_start_end_index():
    # 得到前端传回的参数

    start = request.values.get('start', 0)
    end = request.values.get('end', 0)
    code = json.loads(request.values.get('code'))
    index_lst = json.loads(request.values.get('index_lst'))
    code = code[0]

    res_dict = {}
    res_dict['start'] = [start]
    res_dict['end'] = [end]

    # 组合
    sqli1 = '''SELECT 日期,组合代码,组合累计收益率 FROM [riskgroup].[dbo].[RISK_组合业绩表] where 组合代码 ='%s' and 日期 >= '%s' and 日期 <= '%s' order by 日期 asc''' % (
        code, start, end)
    portfolio_return_df = pd.read_sql(sqli1, conn)

    res_dict['date'] = list(portfolio_return_df['日期'])
    # 日期转换为 年/月/日
    for i in range(len(res_dict['date'])):
        res_dict['date'][i] = res_dict['date'][i][:4] + '-' + res_dict['date'][i][4:6] + '-' + res_dict['date'][i][6:]


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

    sqli2 = '''SELECT 日期,基准名称,基准代码,基准累计收益率 FROM [riskgroup].[IA].[RISK_基准业绩表] 
            where 日期 >= '%s' and 日期 <= '%s' and 基准代码 in (%s) and 组合代码 = '%s' order by 日期 asc''' % (
        start, end, index_str, code)
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



@main.route('/correct/graph1/get_index')
def get_index():
    code = request.values.get('code', 0)
    end = request.values.get('end', 0)
    sqli1 = '''select 基准模式 FROM [riskgroup].[CICC_IA].[组合信息表] where 组合编号 = '%s'    ''' % (code)

    index_df = pd.read_sql(sqli1, conn)
    index_lst = list(index_df['基准模式'])[0].split('/')
    if '' in index_lst:
        index_lst.remove('')

    sqli2 = ''' SELECT 基准编号,名称,基准用途 FROM [riskgroup].[CICC_IA].[业绩基准表] where 起始日期 <= '%s' and isnull(截止日期, '99991231') > '%s' ''' %(end, end)
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



@main.route('/correct/graph1/get_start_end')
def get_start_end():
    # 得到前端传回的参数
    start = request.values.get('start', 0)
    end = request.values.get('end', 0)
    # 数组从前端传回json化, 因此需要json.loads()
    code_lst = json.loads(request.values.get('code_lst'))

    # 将code_lst转化为code_str方便数据库调用
    for i in range(len(code_lst)):
        code_lst[i] = '\'' + code_lst[i] + '\''
    code_str = ','.join(code_lst)

    sqli = '''SELECT 日期,组合代码,组合累计收益率 FROM [riskgroup].[dbo].[RISK_组合业绩表] where 组合代码 in (%s) and 日期 >= '%s' and 日期 <= '%s' order by 日期 asc''' % (
        code_str, start, end)
    portfolio_return_df = pd.read_sql(sqli, conn)
    code = portfolio_return_df['组合代码'].unique()

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



@main.route('/correct/graph1/get_code_lst', methods=['GET','POST'])
def get_code_lst():
    sqli = '''SELECT DISTINCT 组合代码 FROM [riskgroup].[dbo].[RISK_组合业绩表] order by 组合代码 asc'''
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



@main.route('/correct')
def correct():
    return render_template('YYRating/correct.html')

@main.route('/correct/graph1')
def graph1():
    return render_template('YYRating/graph1.html')

@main.route('/correct/graph2')
def graph2():
    return render_template('YYRating/graph2.html')
