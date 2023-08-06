import xlsxwriter, string, openpyxl, os, math
from pylib import collection_util, file_util


# arr:需要循环加字母的数组
# level：需要加的层级
def cycle_letter(arr, level):
    tempArr = []
    letterArr = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', \
                 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    arrNum = len(arr)
    if (level == 0 or arrNum == 0):
        return letterArr
    for index in range(arrNum):
        for letter in letterArr:
            tempArr.append(arr[index] + letter)
    return tempArr


# arr:需要生成的Excel列名称数目
def reduce_excel_col_name(num):
    tempVal = 1
    level = 1
    while (tempVal):
        tempVal = num / (math.pow(26, level))
        if (tempVal > 1):
            level += 1
        else:
            break

    excelArr = []
    tempArr = []
    for index in range(level):
        tempArr = cycle_letter(tempArr, index)
        for numIndex in range(len(tempArr)):
            if (len(excelArr) < num):
                excelArr.append(tempArr[numIndex])
            else:
                return excelArr
    return excelArr


def write_list_list_to_csv(list_list, file, titles=[], encoding='utf-8'):
    output = open(file, 'w', encoding=encoding)
    if len(titles) > 0:
        titlestr = '\t'.join(titles)
        output.write(titlestr + '\n')
    for i in range(len(list_list)):
        for j in range(len(list_list[i])):
            output.write(str(list_list[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
            output.write('\t')  # 相当于Tab一下，换一个单元格
        output.write('\n')  # 写完一行立马换行
    output.close()


# data=[[],[]]
def write_list_list_to_excel(data, file, titles=[], start_row=1, encoding='utf-8'):
    print('data:', data)
    workbook = xlsxwriter.Workbook(file, {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})

    # letter_list = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
    letter_list = reduce_excel_col_name(len(titles))
    print('letter_list:', letter_list)

    for i, title in enumerate(titles):
        # Write some data headers.
        worksheet.write(letter_list[i] + '1', title, bold)

    # Write some data to add to plot on the chart.
    # data = [
    #     [1, 2, 3, 4, 5],
    #     [2, 4, 6, 8, 10],
    #     [3, 6, 9, 12, 15],
    # ]

    for i, title in enumerate(titles):
        # 按列插入
        print(i, title)
        print(data[i])
        worksheet.write_column(row=start_row + 1, col=i, data=data[i])

    # Create a new Chart object.
    # chart = workbook.add_chart({'type': 'column'})
    # Configure the chart. In simplest case we add one or more data series.
    # chart.add_series({'values': '=Sheet1!$A$1:$A$5'})
    # chart.add_series({'values': '=Sheet1!$B$1:$B$5'})
    # chart.add_series({'values': '=Sheet1!$C$1:$C$5'})

    # Insert the chart into the worksheet.
    # worksheet.insert_chart('A7', chart)

    workbook.close()


def append_dict_list_to_excel(data, file, titles=[], encoding='utf-8'):
    if not os.path.exists(file):
        write_dict_list_to_excel(data, file, titles, 1)
    # 以只读模式读取
    wb = openpyxl.load_workbook(file, read_only=True)
    # 新建一个工作薄
    wb = openpyxl.Workbook()

    # 获取当前正在使用的sheet页
    ws = wb.active
    # 获取所有行或列，返回generator
    rows = ws.rows
    columns = ws.columns
    index = len(rows)

    write_dict_list_to_excel(data, file, titles, index)


def write_dict_list_to_excel(data, file, titles=[], start_row=1, encoding='utf-8'):
    print('titles:', titles)
    list = collection_util.convert_dict_list_to_list_list(data, titles)
    print("list:", list)
    write_list_list_to_excel(list, file, titles, start_row, encoding)


def export_to_html_table(table_title, colume_title=[], data_list=[]):
    from HTMLTable import (
        HTMLTable,
    )

    # 标题
    table = HTMLTable(caption=table_title)

    title_tuple = (tuple(colume_title),)
    print(title_tuple)
    # 表头行
    table.append_header_rows(title_tuple)

    # list = [['荔枝', 11, 1, 10],['荔枝2', 11, 1, 10]]
    # tp = collection_util.convert_list_list_to_tuple_tuple(list)
    # print(tp)

    tps = collection_util.convert_list_list_to_tuple_tuple(data_list)
    print(tps)

    # 数据行
    table.append_data_rows(tps)

    # 标题样式
    table.caption.set_style({
        'font-size': '15px',
    })

    # 表格样式，即<table>标签样式
    table.set_style({
        'border-collapse': 'collapse',
        'word-break': 'keep-all',
        'white-space': 'nowrap',
        'font-size': '14px',
    })

    # 统一设置所有单元格样式，<td>或<th>
    table.set_cell_style({
        'border-color': '#000',
        'border-width': '1px',
        'border-style': 'solid',
        'padding': '5px',
    })

    # 表头样式
    table.set_header_row_style({
        'color': '#fff',
        'background-color': '#48a6fb',
        'font-size': '18px',
    })

    # 覆盖表头单元格字体样式
    table.set_header_cell_style({
        'padding': '15px',
    })

    # 调小次表头字体大小
    table[1].set_cell_style({
        'padding': '8px',
        'font-size': '15px',
    })

    # 遍历数据行，如果增长量为负，标红背景颜色
    for row in table.iter_data_rows():
        if row[2].value < 0:
            row.set_style({
                'background-color': '#ffdddd',
            })

    html = table.to_html()
    print(html)
    file_util.write_file(table_title + '.html', html)


if __name__ == '__main__':
    # write_list_list_to_excel([], 'test.xlsx', titles=['a', 'b', 'c'])
    data = [['荔枝', 11, 1, 10],
            ['芒果', 9, -1, -10],
            ['香蕉', 6, 1, 20]]
    export_to_html_table('果园', ['名称', '产量 (吨)', '环比', ''], data)
