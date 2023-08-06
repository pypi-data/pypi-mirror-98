import pymongo
from pymongo import MongoClient


# 获得集合连接
def collection(host, port=27017, db=None, user_name=None, password=None, col_name=None):
    client = pymongo.MongoClient(host=host, port=port)
    mdb = client[db]
    mdb.authenticate(user_name, password)
    col = mdb[col_name]
    return col


# 主键冲突插入不报错
def insertSilent(collection={}, query={}, data={}):
    collection.update(query, {'$setOnInsert': data}, True)


# 插入或更新
def insertOrUpdate(collection={}, query={}, insert={}, update={}):
    if insert:
        collection.update(query, {'$setOnInsert': insert}, True)
        # collection.update(query, {'$setOnInsert': insert, '$set': update}, True)
    else:
        collection.update(query, {'$set': update}, True)


# 创建索引
def create_index(col, field):
    col.create_index([(field, -1)], unique=True)


def find(col, query={}, ret_field=[], sort_by={}, limit=()):
    field = {}
    for item in ret_field:
        field[item] = 1
    result = col.find(query, field).sort([("created_at", pymongo.ASCENDING)]).limit(limit).skip(0)
    # result = self.fund.find({'type': '指数型'}, {'id': 1, 'fundSName': 1}).sort('total_assets', -1).limit(100)
    ret_list = list(result)
    return ret_list


# 将MongoDB的结果转换为list，不直接用list(result[:]),是因为直接list强转不能识别limit
def convert_result_list(result):
    list = []
    i = 0
    for item in result:
        i += 1
        # print(i, item)
        list.append(item)
    return list
