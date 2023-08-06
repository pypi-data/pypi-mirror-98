from bs4 import BeautifulSoup


# 匹配出所有标记，并返回标记的结果属性，
def match_tag_attr_list(html, html_tag, ret_tag_attr=None):
    soup = BeautifulSoup(html, 'html5lib')
    tags = soup.findAll(html_tag)
    list = []
    for t in tags:
        if ret_tag_attr:
            list.append(t.get(ret_tag_attr))
        else:
            list.append(t.contents)
            # print(t.get(ret_tag_attr))
            # print(t.contents)
    return list

# 返回html中所有表格
def match_table(html):
    soup = BeautifulSoup(html, 'html5lib')
    table = soup.findAll('table')
    print(table)

# 匹配到对象列表
def match_tag_list_by_xpath(html, xpath):
    soup = BeautifulSoup(html, 'lxml')
    # print(html)
    # xpath = 'ul.sellListContent > li.clear.LOGCLICKDATA'
    lis = soup.select(xpath)
    # for li in lis:
    #     print(li)
    return lis

# 返回匹配到的第一个tag对象
def match_tag_first_by_xpath(html, xpath):
    list = match_tag_list_by_xpath(html, xpath)
    if list:
        return list[0]
    return None
