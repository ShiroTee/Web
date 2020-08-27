import pymssql as ms
from config import DB


# 1. 创建连接
conn = ms.connect(DB.HOST, DB.USER, DB.PASSWD, DB.DBNAME)
cur = conn.cursor()



def isUserExist(username):
    """判断用户名是否存在"""
    sqli = '''select * from [riskgroup].[IA].[flask_test] where name='%s' '''% (username)
    cur = conn.cursor()
    cur.execute(sqli)
    if len(cur.fetchall()) == 0:
        return False
    else:
        return True


def isPasswdOk(username, passwd):
    sqli = "select * from [riskgroup].[IA].[flask_test] where name='%s' and [passwd]='%s'" %(
        username, passwd)
    cur = conn.cursor()
    cur.execute(sqli)

    if len(cur.fetchall()) == 0:
        return False
    else:
        return True


def addUser(username, passwd):
    """用户注册时， 添加信息到数据库中"""
    sqli = "insert into [riskgroup].[IA].[flask_test](name, passwd) values('%s', '%s')" %(
        username, passwd)
    try:
        res = cur.execute(sqli)
        conn.commit()
    except Exception as e:
        conn.rollback()
        return e
#
# cur.close()
# conn.close()
if __name__ == "__main__":
    addUser('root', 'root')
