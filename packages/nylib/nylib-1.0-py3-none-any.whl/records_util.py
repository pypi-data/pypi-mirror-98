import pymysql

pymysql.install_as_MySQLdb()
import records
from . import url_util


def init_mysql_url(host, username, password, port, db):
    url = 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        url_util.urlencode(username), url_util.urlencode(password), host, port, db)
    return url


def conn(dburl):
    db = records.Database(
        dburl,
        encoding="utf-8", echo=False)
    return db


def exe_sql(db_conn, sql):
    rows = db_conn.query(sql)
    return rows


def query(url, sql, echo=False):
    db = records.Database(url, encoding="utf-8", echo=False)
    rows = db.query(sql)
    return rows


# 将record的结果转为[{}]
def record_result_to_dict_list(rows):
    ret = []
    for row in rows:
        keys = row.keys()
        values = list(row.values())

        dic = dict(zip(keys, values))
        # print(dic)
        ret.append(dic)
    return ret
