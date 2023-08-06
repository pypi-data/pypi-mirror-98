import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame


# 不错的教程 https://www.jianshu.com/p/6eb5499cd07d


# 将excel单sheet中的二维表读取到list的对象中
def read_excel_sheet(excel_path, sheet_name, titles=[], skiprows=0):
    ret = []
    df = pd.read_excel(excel_path, sheet_name=sheet_name, skiprows=skiprows)

    for index, row in df.iterrows():
        obj = {}
        if len(titles) == 0:
            titles = row.keys()
        for t in titles:
            obj[t] = row[t]
        ret.append(obj)
    return ret


# 返回整个excel所有sheet表格，resutl[sheet1]=[{a:1,b:2}]
def read_excel_sheets(excel_path, skiprows=0):
    ret = {}

    df = pd.read_excel(excel_path, sheet_name=None, skiprows=skiprows)
    # 遍历工作表
    for k in df.keys():
        list = []
        # print(df)
        for index, row in df[k].iterrows():
            obj = {}
            for t in row.keys():
                # print(t)
                obj[t] = row[t]
            list.append(obj)
        ret[k] = list
    return ret


# 将list[dict]对象转换为df
def convert_list_to_dataframe(list=[]):
    # 将 list 转为 dict
    # 将 dict 转为 Dataframe
    # 写入到 excel 里。
    fields = []
    if len(list) > 0:
        fields = list[0].keys()

    dict = {}
    # 初始化每个字段的列表
    for f in fields:
        dict[f] = []

    for item in list:
        for k in item.keys():
            # 给字典中填充列表数据
            dict[k].append(item[k])

    df = DataFrame(dict)
    print(df)
    return df


# 将df转换为list[[123],[223]]格式
def convert_dataframe_to_list_list(df):
    train_data = np.array(df)  # np.ndarray()
    # print(train_data)
    train_x_list = train_data.tolist()  # list
    return train_x_list


# 将df转换为list[{a:1},{a:2}]格式, headers 表示需要重新指定的标题列表
def convert_dataframe_to_dict_list(df, headers=[]):
    # dfname._stat_axis.values.tolist()  # 行名称
    # dfname.columns.values.tolist()  # 列名称

    header_list = df.columns.values.tolist() if len(headers) == 0 else headers
    # print(header_list)
    list_list = convert_dataframe_to_list_list(df)
    # print(list_list)

    # >>> d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    # >>> d
    # {'a': 1, 'c': 3, 'b': 2, 'd': 4}
    # >>> d.keys()
    # ['a', 'c', 'b', 'd']
    # >>> d.values()
    # [1, 3, 2, 4]
    # >>> zip(d.values(),d.keys())
    # [(1, 'a'), (3, 'c'), (2, 'b'), (4, 'd')]
    # >>> dict(zip(d.values(),d.keys()))
    # {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

    # 先遍历rows里面的值，然后在用zip反转
    dict_list = [dict(zip(header_list, row)) for row in list_list] if list_list else None
    # print(dict_list)
    return dict_list


# 将list[dict]对象写入excel单sheet表
def write_excel(list=[], excel_path=""):
    df = convert_list_to_dataframe(list)
    df.to_excel(excel_path)


# 将dict{list[dict]}对象写入excel多sheet表
def write_excel_sheets(dict={}, excel_path=""):
    write = pd.ExcelWriter(excel_path)

    fields = dict.keys()

    for (sheet, list) in dict.items():
        df = convert_list_to_dataframe(list)
        df.to_excel(write, sheet_name=sheet, header=fields, index=False)
    write.save()


# 将dataframe数据集写入到excel中
def write_df_to_excel(df, excel_path="", sheet_name='Sheet1'):
    writer = pd.ExcelWriter(excel_path)
    df.to_excel(writer, index=True, encoding='utf-8', sheet_name=sheet_name)
    writer.save()


# 将多个df合并追加
def append_dataframe(dst_df, source_df, ignore_index=False):
    if dst_df is None:
        dst_df = source_df
    else:
        dst_df = dst_df.append(source_df, ignore_index=ignore_index)
    return dst_df


def new_dataframe(column_names=[], rows_list=[]):
    df = pd.DataFrame(columns=column_names, data=rows_list)
    return df


def test():
    # 读取Excel的第一个表单

    df = pd.read_excel('demo1.xlsx')

    # 输出列标题

    print(df.columns.values)

    # 第第1行数据(不包含表头)

    data = df.loc[0].values

    print(data)

    # 第2~3行的数据

    data = df.loc[[1, 2]].values

    print(data)

    data = {"姓名": ["程序猿", "程旭阳", "陈续员"], "性别": ["男", "女", "未知"],

            "年龄": [50, 55, 60], "课程": ["Python", "学不懂", "学不动"]}

    df = pd.DataFrame(data)


if __name__ == '__main__':
    excel_path = "/Users/jinlong.rhj/Downloads/2019年2月班级人数表（含学籍号） - 副本.xlsx"
    res = read_excel_sheets(excel_path, 1)
    print(res['一年级'])
    write_excel(res['一年级'], '/Users/jinlong.rhj/Downloads/bbb.xlsx')
    # convert_list_to_dataframe(res['一年级'])
    write_excel_sheets(res, '/Users/jinlong.rhj/Downloads/ccc.xlsx')




    # # #按行求和
    # df['row_sum'] = df.apply(lambda x: x.sum(), axis=1)
    #
    # #按列求和
    # df.loc['col_sum'] = df.apply(lambda x: x.sum())
