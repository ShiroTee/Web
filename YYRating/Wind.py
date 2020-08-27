#运行环境依赖Wind终端
from WindPy import *
w.start()

#运行逻辑(以每周六运行为例):
#起始日期: 当天的日历日一周前的下一个交易日
#终止日期: 当天的上一个交易日

def get_start_end_date():
    # today = datetime.datetime.now().strftime('%Y-%m-%d')
    today = '2020-07-04'
    last_week = w.tdaysoffset(-1, today, "Days=Alldays;Period=W").Data[0][0].strftime('%Y-%m-%d')

    start = w.tdaysoffset(1, last_week, "").Data[0][0].strftime('%Y-%m-%d') #后 从1开始
    end = w.tdaysoffset(0, today, "").Data[0][0].strftime('%Y-%m-%d') #前 从0开始

    return start, end