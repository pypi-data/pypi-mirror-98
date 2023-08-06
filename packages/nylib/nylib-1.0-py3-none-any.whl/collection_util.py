import random, types

from operator import itemgetter
from itertools import groupby


# 去除空字符元素
def removeEmpty(arr):
    while '' in arr:
        arr.remove('')
    return arr


# 合并数组
def merge_list(a, b):
    ret = []
    for i in a:
        ret.append(i)
    for i in b:
        ret.append(i)
    return ret


# 合并数组并排序
def merge_sort(a, b):
    ret = []
    while len(a) > 0 and len(b) > 0:
        if a[0] <= b[0]:
            ret.append(a[0])
            a.remove(a[0])
        if a[0] >= b[0]:
            ret.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        ret += b
    if len(b) == 0:
        ret += a
    return ret


# 递归的方法比较容易理解
def expand_list(nested_list=[[], []]):
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            for sub_item in expand_list(item):
                yield sub_item
        else:
            yield item

            #
            # # 在stackoverflow看到大牛的列表生成式版本
            # func = lambda x: [y for l in x for y in func(l)] if type(x) is list else [x]


# 数组随机排序
def random_sort(list=[]):
    random.shuffle(list)
    return list


# 过滤数组
def filter_list(func, listdata=[]):
    return list(filter(func, listdata))


# 将大list按大小拆分为多个小list
def split_list_to_group(listdata=[], n=1):
    # 大列表中几个数据组成一个小列表
    # ret = []
    ret = [listdata[i:i + n] for i in range(0, len(listdata), n)]
    return ret


def foreach_list(func, list=[]):
    # print(type(func) is types.FunctionType)
    ret = []
    for i, value in enumerate(list):

        if func.__code__.co_argcount == 2:
            item = func(value, i)
        else:
            item = func(value)
        if item:
            ret.append(item)
    return ret


def foreach_dict(func, dict={}):
    ret = []
    if func.__code__.co_argcount == 3:
        for i, k in enumerate(dict.keys()):
            v = dict[k]
            item = func(k, v, i)
            if item:
                ret.append(item)
    else:
        for k, v in dict.items():
            item = func(k, v)
            if item:
                ret.append(item)
    return ret


def get_dict_keys(dic={}):
    ret = []
    for k, v in dic.items():
        ret.append(k)
    return ret


# 将内字典外列表，转为内列表外字典,每个key是一列
def convert_dict_list_to_list_dict(list=[]):
    dict = {}
    if len(list) > 0:
        dict = list[0]

    def append_dict(dict={}, item={}):
        keys = dict.keys()

        for k in keys:
            sublist = dict[k] if type(dict[k]).__name__ == 'list' else []

            sublist.append(item.get(k, None))
            dict[k] = sublist

    for i, item in enumerate(list):
        append_dict(dict, item)

    return dict


# 将内字典外列表，转为内列表外列表,二维表：内列表是一列，有多少个子列表就有多少行
def convert_dict_list_to_list_list(list=[], keys=[]):
    dic = convert_dict_list_to_list_dict(list)
    if len(keys) == 0:
        keys = dic.keys()

    ret = []
    for key in keys:
        ret.append(dic.get(key))

    return ret


# 将内列表外列表，转为内列表外字典
def convert_list_list_to_list_dict(list=[], keys=[]):
    dict = {}

    def append_dict(dict={}, item={}, keys=[]):

        for i, k in enumerate(keys):
            sublist = dict.get(k, [])

            sublist.append(item[i])
            dict[k] = sublist

            # break

    for i, item in enumerate(list):
        append_dict(dict, item, keys)
        # break

    return dict


# 将内列表外列表，转为内字典外列表
# 转换前：每个子列表为一列，有多少列就有几个子列表
# 转化后：每个子字典为一行，多个字典就是多行
def convert_columnlist_list_to_dict_list(list=[[]], keys=[]):
    ret = []

    row_count = len(list[0])

    for i in range(1, row_count):
        dict = {}
        for j, k in enumerate(keys):
            # print(j, k, len(list))
            dict[k] = list[j][i] if len(list) - 1 >= j else None
        ret.append(dict)

    return ret


def convert_list_to_tuple(list=[]):
    return tuple(list)


def convert_list_list_to_tuple_tuple(list=[]):
    ret = ()
    for item in list:
        print(ret)
        tp = tuple(item)
        if len(ret) == 0:
            ret = ((tp),)
        else:
            ret = ret + (tp,)
    return ret


# 过滤列表
def filter_list(judge_func, list=[]):
    return filter(judge_func, list)


# 按某个key取出字典列表中的值组成列表返回
def filter_dict_list_to_list(list=[], key=''):
    ret = []
    for item in list:
        obj = item.get(key, None)
        ret.append(obj)
    return ret


# 删除字典列表中字典的某个字段
def del_field_in_dict_list(list=[], key=''):
    ret = []
    for item in list:
        if key in item.keys():
            del item[key]
        ret.append(item)
    return ret


# 给字典数组加上一列相同的值
def add_dict_field_to_dict_list(list=[], key='', value=None):
    ret = []
    for item in list:
        item[key] = value
        ret.append(item)
    return ret


# # 给字典数组加上一列相同的值
# def fill_default_field_to_dict_list(list=[], key='', value=None):
#     ret = []
#     for item in list:
#         item[key] = value
#         ret.append(item)
#     return ret

# 将字典转成成数组
def convert_dict_to_list_list(dict={}):
    keys = []
    values = []
    for k, v in dict.items():
        keys.append(k)
        values.append(v)
    return [keys, values]


# 按key将列表分组
def groupByKey(rows=[{}], keyName=''):
    ret = {}
    for gp, items in groupby(rows, key=itemgetter(keyName)):
        # print(gp)
        for item in items:
            # print(item)
            ret[gp] = item
            break

    return ret


def merge_two_dicts(a, b):
    c = a.copy()  # make a copy of a
    c.update(b)  # modify keys and values of a with the ones from b
    return c


def merge_dictionaries(a, b):
    return {**a, **b}


def to_dict(keys=[], values=[]):
    return dict(zip(keys, values))


# spread([1,2,3,[4,5,6],[7],8,9]) # [1,2,3,4,5,6,7,8,9]
def spread(arg=[]):
    ret = []
    for i in arg:
        if isinstance(i, list):
            ret.extend(i)
        else:
            ret.append(i)
    return ret


if __name__ == '__main__':
    # a = [1, 3, 4, 6, 7, 78, 97, 190]
    # b = [2, 5, 6, 8, 10, 12, 14, 16, 18]
    #
    # print(merge_sort(a, b))
    # list = [{'a': 1, 'b': 2}, {'a': 1, 'b': 2}]
    # dict = convert_dict_list_to_list_dict(list)
    # print(dict)

    # l = [i for i in range(15)]
    # n = 3  # 大列表中几个数据组成一个小列表
    # ret = ([l[i:i + n] for i in range(0, len(l), n)])
    # print(ret)

    rows = [
        {'address': '5412 N CLARK', 'date': '07/01/2012'},
        {'address': '5148 N CLARK', 'date': '07/04/2012'},
        {'address': '5800 E 58TH', 'date': '07/02/2012'},
        {'address': '2122 N CLARK', 'date': '07/03/2012'},
        {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
        {'address': '1060 W ADDISON', 'date': '07/02/2012'},
        {'address': '4801 N BROADWAY', 'date': '07/01/2012'}]
    print(groupByKey(rows, 'date'))
