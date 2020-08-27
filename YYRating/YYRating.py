import re
import os
import time
import datetime
import logging
import pandas as pd
import configparser
import pymssql as ms
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from Wind import get_start_end_date

# Selenium三种等待方式
# 1. time.sleep()
#    强制等待

# 2. driver.implicitly_wait(30)
#    隐性等待，全局等待，最长等待30秒，如果全局元素加载好，结束等待(本程序没有使用到)

# 3. wait = WebDriverWait(driver, 10)
#    wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//input[@placeholder="请输入代码、简称、发行人"]')))
#    显性等待，指定元素等待，最长等待10秒，如果指定元素加载好，结束等待(本程序基本使用显性等待，以XPATH指定)


# 循环体
def loop(issuer_list):
    error_issuer = [] # 存储出错的发行人
    # 获取游标
    cursor = connect.cursor()

    try:
        for i in range(len(issuer_list)):
            current_issuer = issuer_list[i][0]  # 当前发行人
            issuer(current_issuer)  # 搜索当前发行人
            issuer_data = get_data(current_issuer, i) # 得到当前发行人的dataframe

            # 删除数据库 起止时间 和 发行人
            start_date = re.sub('\D', '', start)
            end_date = re.sub('\D', '', end)
            sSql1 = '''delete from [riskgroup].[IA].[bond_trans_YYRating_test] where 成交日期 >= '%s' and 成交日期 <= '%s' and 发行人 = '%s' ''' % (
            start_date, end_date, current_issuer)
            cursor.execute(sSql1)
            connect.commit()

            # 得到数据库存入的values_tuple
            for j in issuer_data.values.tolist():
                for k in range(len(j)):
                    if isinstance(j[k], str):
                        j[k] = j[k].strip()
                        # 如果为'-' 设为空值
                        if j[k] == '-':
                            j[k] = None
                j.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # 加入入库时间
                j = tuple(j)

                # 插入数据库
                sSql2 = '''insert into [riskgroup].[IA].[bond_trans_YYRating_test](成交日期,
                        债券简称,
                        发行人,
                        剩余期限,
                        成交价,
                        收益率,
                        成交量,
                        成交额,
                        YY等级,
                        成交隐含,
                        YY偏离,
                        偏离,
                        是否汇总,
                        债券类型,
                        发行方式,
                        数据来源,
                        交易市场,
                        主体类型,
                        债券代码,
                        入库时间) values (%s, %s, %s, %s, %d, %d, %d, %d, %s, %s, %s, %d, %s, %s, %s, %s, %s, %s, %s, %s)''' # %d 即为float型
                cursor = connect.cursor()
                cursor.execute(sSql2, j)
                connect.commit()

        logging.info('End of spiders!')
    except (TimeoutException, NoSuchElementException):
        error_issuer.append(issuer_list[i][0])

    # 将出错的发行人输出到日志
    if len(error_issuer) != 0:
        for item in error_issuer:
            logging.warning('Issuer {} needs to reload!'.format(item))
    else:
        logging.info('No error exists!')

# 选择发行人
def issuer(i):
    time.sleep(1.5)
    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[@placeholder="请输入代码、简称、发行人"]')))
    input.clear()
    time.sleep(1.5)
    input.clear()
    input.send_keys('{}'.format(i))

    return_page()
    time.sleep(5)

# 点击查询
def return_page():
    time.sleep(1.5)
    submit_search = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="el-button el-button--primary"]')))
    time.sleep(1.5)
    submit_search.click()





# 登陆
def login(start, end):
    # 手机号码登录
    submit1 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class="tc el-col el-col-5"]//a')))
    submit1.click()

    submit2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class="footer el-row"]//div[2]')))
    submit2.click()

    # 输入账号密码
    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[@placeholder="手机号码"]')))
    input.send_keys('18620313666')

    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//div[@class="el-input el-input--suffix"]//input[@class="el-input__inner"]')))
    input.send_keys('test123')

    # 点击登陆
    submit3 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class="el-col el-col-12"]//button[@class="el-button el-button--primary"]//span')))
    submit3.click()

    # 前台成交页面
    driver.get('https://www.ratingdog.cn/#/rating/frontDeskDeal?index=3-2')

    # 勾选私募
    # time.sleep(1.5)
    # submit5 = wait.until(EC.element_to_be_clickable(
    # (By.XPATH, '//div[@class="filter"]//div[2]//div[1]//div[1]//label[2]')))
    # time.sleep(1.5)
    # submit5.click()

    # 勾选公募
    # time.sleep(1.5)
    # submit6 = wait.until(EC.element_to_be_clickable(
    # (By.XPATH, '//div[@class="filter"]//div[2]//div[1]//div[1]//label[1]')))
    # time.sleep(1.5)
    # submit6.click()

    # 下拉
    time.sleep(1.5)
    submit7 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//i[@class="el-icon-d-arrow-left negative"]')))
    time.sleep(1.5)
    submit7.click()

    # 选择上一周
    select_time(start, end)

    # 100条/页
    change_to_100()

# 输入起止时间
def select_time(start, end):
    time.sleep(1.5)
    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[@placeholder="起始日期"]')))
    input.clear()
    time.sleep(1.5)
    input.clear()
    input.send_keys('{}'.format(start))

    time.sleep(1.5)
    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[@placeholder="结束日期"]')))
    input.clear()
    time.sleep(1.5)
    input.clear()
    input.send_keys('{}'.format(end))

# 改成100条/页
def change_to_100():
    time.sleep(1.5)
    submit_100pages = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@placeholder="请选择"]')))
    time.sleep(1.5)
    submit_100pages.click()

    try:
        time.sleep(1.5)
        submit_100pages = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="el-select-dropdown el-popper"]//li[3]')))
        time.sleep(1.5)
        submit_100pages.click()

    except TimeoutException:
        time.sleep(1.5)
        submit_100pages = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//li[@class="el-select-dropdown__item selected hover"]//span[contains(text(),"100")]')))
        time.sleep(1.5)
        submit_100pages.click()



# 在当前界面查询一个发行人的所有页面数据（小于300）
def get_data(issuer, i):
    # if WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//span[contains(@class,"el-table__empty-text")]'),
    # '没有找到匹配的记录！')):
    # df1 = pd.DataFrame()
    # print('Issuer No.{}--{} has {} data. 数据为0 .'.format(i, issuer, df1.shape[0]))
    # return df1
    try:
        # 显性等待15s 若出错 则说明当前页面无数据
        # 这里判断发行人的元素位置文本是否是当前发行人
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.XPATH, '//tr[1]//td[4]//div[1]//div[1]//a[1]//span[1]'),
                                             '{}'.format(issuer)))
        try:
            time.sleep(1.5)
            total = get_num_of_data()  # 不超过一百个将报错
            #time.sleep(5)
            if total <= 300:
                df1 = search_page(1)  # 第一页的数据
                pages = total // 100
                if pages == 1:
                    df2 = search_page(2) # 第二页的数据
                    time.sleep(1.5)
                    df1 = pd.concat([df1, df2], axis=0)
                    if df1.shape[0] == total:
                        logging.info('Issuer No.{}--{} has {} data. Correct!'.format(i, issuer, total))
                    else:
                        logging.info('Issuer No.{}--{}. Error! Not match!'.format(i, issuer))
                elif pages == 2:
                    df2 = search_page(2) # 第二页的数据
                    time.sleep(1.5)
                    df1 = pd.concat([df1, df2], axis=0)
                    df2 = search_page(3) # 第三页的数据
                    time.sleep(1.5)
                    df1 = pd.concat([df1, df2], axis=0)
                    if df1.shape[0] == total:
                        logging.info('Issuer No.{}--{} has {} data. Correct!'.format(i, issuer, total))
                    else:
                        logging.info('Issuer No.{}--{}. Error! Not match!'.format(i, issuer))
            else:
                logging.info('Issuer No.{}--{} has more than 300 data. Error!'.format(i, issuer))

        except NoSuchElementException:
            df1 = get_DataFrame_from_each_page(driver)
            logging.info('Issuer No.{}--{} has {} data. 数据大于0小于100'.format(i, issuer, df1.shape[0]))

    except TimeoutException:
        df1 = pd.DataFrame()
        logging.info('Issuer No.{}--{} has {} data. 数据为0 .'.format(i, issuer, df1.shape[0]))

    return df1

# 得到总共有多少条数据
def get_num_of_data():
    # 找到元素位置
    totalCount = driver.find_element_by_class_name('el-pagination__total').text
    totalCount = int(re.sub('\D','',totalCount))
    return totalCount

# 选择页面的函数 i是页码(2 or 3)
def search_page(i):
    #time.sleep(5)

    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//div[@class="el-input el-pagination__editor is-in-pagination"]//input[@class="el-input__inner"]')))
    input.clear()
    time.sleep(1.5)
    input.clear()
    input.send_keys('{}'.format(i))

    # 找到元素位置
    input_Tag = driver.find_element_by_xpath(
        '//div[@class="el-input el-pagination__editor is-in-pagination"]//input[@class="el-input__inner"]')
    input_Tag.send_keys(Keys.ENTER)
    # 点击查询，需要时间等待页面加载，故这里time.sleep(5)稍长
    time.sleep(5)

    return get_DataFrame_from_each_page(driver)

# 得到DataFrame的函数
def get_DataFrame_from_each_page(driver):
    # 得到html源码
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    trs = soup.find_all('tr')
    # 得到每一个td 即 表格中的一个元素
    list0 = []
    for tr in trs:
        list1 = []
        tds = tr.find_all('td')
        for td in tds:
            list1.append(td.get_text())
        list0.append(list1)
    data_page = pd.DataFrame(list0)
    # data_page.columns = ['序号','成交日期','债券简称','发行人','剩余期限','成交价(元)',"收益率",'成交量(手)','成交额(万元)','YY等级','成交隐含',
    # 'YY偏离(BP)','偏离(BP)','是否汇总','债券类型','发行方式','数据来源','交易市场','主体类型','债券代码']
    data_page.columns = ['序号', '成交日期', '债券简称', '发行人', '剩余期限', '成交价', "收益率", '成交量', '成交额', 'YY等级', '成交隐含',
                         'YY偏离', '偏离', '是否汇总', '债券类型', '发行方式', '数据来源', '交易市场', '主体类型', '债券代码']
    # drop掉无用行
    data_page = data_page.dropna(subset=['债券代码'])

    # 将成交日期整理为8位
    tool1 = list(data_page['成交日期'])
    for i in range(1, data_page['成交日期'].shape[0] + 1):
        data_page['成交日期'][i] = re.sub('\D', '', data_page['成交日期'][i])

    # 转换为numeric
    data_page["成交价"] = pd.to_numeric(data_page["成交价"])
    data_page["收益率"] = pd.to_numeric(data_page["收益率"]) / 100
    data_page["成交量"] = pd.to_numeric(data_page["成交量"])
    data_page["成交额"] = pd.to_numeric(data_page["成交额"])
    data_page["偏离"] = pd.to_numeric(data_page["偏离"])

    # drop掉序号这一列
    data_page = data_page.drop(['序号'], axis=1)

    return data_page



if __name__ == "__main__":
    #创建日志
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    rq = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_path = os.path.split(os.path.realpath('__file__'))[0] + '\\'
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)


    #读取配置文件
    proDir = os.path.split(os.path.realpath('__file__'))[0]
    configPath = os.path.join(proDir, "config.ini")
    path = os.path.abspath(configPath)
    ccon = configparser.ConfigParser()
    ccon.read(path, encoding='UTF-8')

    dbstr = ccon.get('msdb_main', 'msdb_host')
    user = ccon.get('msdb_main', 'msdb_user')
    pwd = ccon.get('msdb_main', 'msdb_pwd')
    db = ccon.get('msdb_main', 'msdb_db')

    #Chromedriver的地址
    Chromedriver_path = ccon.get('Chromedriver', 'Chromedriver_path')

    #连接数据库
    connect = ms.connect(dbstr, user, pwd, db, charset='utf8')
    if connect:
        logging.info('msdb_main连接成功')

    sql = '''select issuer from riskgroup.IA.bond_issuer_YYRating '''
    issuer_pd = pd.read_sql(sql, connect)
    issuer_list = issuer_pd.values.tolist()


    #打开Chrome
    driver = webdriver.Chrome(executable_path=Chromedriver_path + '\\chromedriver.exe')
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    #得到最近一周的时间
    start, end = get_start_end_date()

    #输入网址 登陆到搜索界面
    driver.get('https://www.ratingdog.cn/#/home')
    login(start, end) #这里已经改成100条/页

    #循环体
    loop(issuer_list)

    #关闭数据库连接
    connect.close
    logging.info('Connection close!')