import pymysql
import logging
import sys

# 加入日志
# 获取logger实例
logger = logging.getLogger("baseSpider")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s%(levelname)-8s:%(message)s')
# 文件日志
file_handler = logging.FileHandler("baseSpider.log")
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)


class DBHelper:
    # 构造函数
    def __init__(self, host='127.0.0.1', user='root',
                 pwd='123456', db='testdb', port=3306):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port
        self.conn = None
        # self.cur = None

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd,
                                        database=self.db, port=self.port, charset='utf8')
        except:
            logger.error("connectDatabase failed")
            return False
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True




    def get_conn(self):
        """
        获取连接
        :rtype: object
        """
        return self.conn

    def close_conn(self):
        """
        关闭连接
        :rtype: object
        """
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print(e)

    def query(self, sql, close=True):
        """
        查询sql
        :rtype: object
        """
        self.connectDatabase()
        # 获取cursor
        cursor = self.conn.cursor()
        # 执行sql
        cursor.execute(sql)

        # 拿到结果
        # print(cursor.fetchall())
        res = [dict(zip([x[0] for x in cursor.description], row)) for row in cursor.fetchall()]
        # 关闭cursor
        cursor.close()
        if close:
            # 关闭连接
            self.close_conn()
        return res

    def execute(self, sql, commit=True, close=True):
        """
        执行sql
        :rtype: object
        """
        res = True
        self.connectDatabase()
        # 获取cursor
        cursor = self.conn.cursor()
        try:
            # 执行sql
            cursor.execute(sql)
            if commit:
                self.conn.commit()
        except pymysql.Error as e:
            self.conn.rollback()
            print(e)
            res = False
        # 关闭cursor
        cursor.close()
        if close:
            # 关闭连接
            self.close_conn()
        return res

    def find(self, table, where, field="*", close=True):
        """
        查询单条记录
        :rtype: object
        """
        sql = self.get_select_sql(table, where, field)
        # 获取cursor
        cursor = self.conn.cursor()
        try:
            # 执行sql
            cursor.execute(sql)
            # 拿到结果   dict(zip(['a','b'],(1,2)))  ==> {'a': 1, 'b': 2}  cursor.fetchone 拿到的是这条数据的元祖格式
            res = dict(zip([x[0] for x in cursor.description], cursor.fetchone()))
        except pymysql.Error as e:
            res=str(e)
        # 关闭cursor
        cursor.close()
        if close:
            # 关闭连接
            self.close_conn()
        return res

    def select(self, table, where, field="*", orderby="", page=0, page_size=10, close=True):
        """
        查询多条记录
        :rtype: object
        """
        sql = self.get_select_sql(table, where, field, orderby, page, page_size)
        return self.query(sql, close)

    def insert(self, table, dict, commit=True, close=True):
        """
        插入
        :rtype: object
        """
        sql = self.get_insert_sql(table, dict)
        return self.execute(sql, commit, close)

    def update(self, table, seting, where="", commit=True, close=True):
        """
        更新
        :rtype: object
        """
        sql = self.get_update_sql(table, seting, where)
        return self.execute(sql, commit, close)

    def delete(self, table, where, commit=True, close=True):
        """
        删除
        :rtype: object
        """
        where_string = self.get_where_sql(where)
        sql = "delete from {} {}".format(table, where_string)
        return self.execute(sql, commit, close)

    def get_select_sql(self, table, where="", field="*", orderby='', page=0, page_size=10):
        """
        获取查询sql语句
        :rtype: object
        """
        where_string = self.get_where_sql(where)
        if isinstance(field, list):
            field = ','.join(field)
        sql = "select {} from {} {}".format(field, table, where_string)
        if orderby != '':
            sql = sql.strip() + ' order by ' + orderby
        if page != 0:
            offset = (page - 1) * page_size
            sql = sql + " limit %s,%s" % (offset, page_size)
        return sql.strip() + ';'

    def get_insert_sql(self, table, dict):
        """
        获取插入sql语句
        :rtype: object
        """
        fields = '`' + '`,`'.join(dict.keys()) + '`'
        values = []
        for k in dict.keys():
            v = dict[k]
            if type(v) not in (int, float, str):
                if not v:
                    values.append('')
                else:
                    s = u'值错误, key: {}, value: {}, type: {}'.format(k, v, type(v))
                    raise Exception(s)
            if v == 'now()':
                values.append(v)
            elif type(v) is str:
                values.append("'{}'".format(v.replace('\\', '\\\\')))
            else:
                values.append('{}'.format(v))
        value_str = ','.join(values)
        return 'INSERT INTO {} ({}) VALUE ({});'.format(table, fields, value_str)

    def get_update_sql(self, table, seting, where):
        """
        获取更新sql语句
        :rtype: object
        """
        where_string = self.get_where_sql(where)
        if isinstance(seting, dict):
            tmp = []
            for k, v in seting.items():
                tmp.append(k + " = '" + str(v) + "'")
            set_string = ','.join(tmp)
        else:
            set_string = seting
        return 'update {} set {} {};'.format(table, set_string, where_string)

    def get_where_sql(self, where):
        """
        拼接where查询语句
        :rtype: object
        """
        if isinstance(where, dict):
            tmp = []
            for k, v in where.items():
                tmp.append("and " + str(k) + "='" + str(v) + "' ")
            if tmp != []:
                where_string = 'where' + ''.join(tmp).lstrip('and')
            else:
                where_string = ""
        else:
            where_string = where
        return where_string


if __name__ == '__main__':
    dbhelper = DBHelper()
    # 创建数据库的表
    sql = "create table maoyan('id'varchar(8),\
            'title'varchar(50),\
            'star'varchar(200), \
            'time'varchar(100),primary key('id'));"
    result = dbhelper.execute(sql)
    if result:
        logger.info("maoyan　table创建成功")
    else:
        logger.error("maoyan　table创建失败")
