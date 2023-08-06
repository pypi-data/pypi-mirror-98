import re, urllib
from pylib import request_util, url_util, log_util


def convert_curl_to_array(curl_str):
    header_arr = get_headrs(curl_str)
    # print(header_arr)

    # data_arr = get_data_str(curl_str)
    # print(data_arr)

    url = "'{0}'".format(get_url(curl_str))
    # print(url)
    headers = "-H '" + "' -H '".join(header_arr) + "'"
    # print(headers)
    data = " --data '" + get_data_str(curl_str) + "'"
    # print(data)

    return ['curl', url, headers, data, '--compressed']


# 获取get链接
def get_url(curl_str):
    pattern = re.compile(r'curl \'(.*?)\' ')
    url_arr = re.findall(pattern, curl_str)
    # 一般url不是在前面，就是在后面
    if len(url_arr) == 0:
        pattern = re.compile(r'--compressed \'(.*?)\'')
        url_arr = re.findall(pattern, curl_str)
    return ''.join(url_arr)


# 获取post参数字符串
def get_data_str(curl_str):
    pattern = re.compile(r'--data \'(.*?)\' ')
    data_arr = re.findall(pattern, curl_str)
    return ''.join(data_arr)


def get_data_binary_str(curl_str):
    pattern = re.compile(r'--data-binary \'(.*?)\' ')
    data_arr = re.findall(pattern, curl_str)
    return ''.join(data_arr)


def get_data_raw_str(curl_str):
    pattern = re.compile(r'--data-raw \'(.*?)\' ')
    data_arr = re.findall(pattern, curl_str)
    return ''.join(data_arr)


# 获取header数组
def get_headrs(curl_str):
    pattern = re.compile(r'-H \'(.*?)\' ')
    header_arr = re.findall(pattern, curl_str)
    return header_arr


# 获取header对象
def get_header_map(curl_str):
    header_arr = get_headrs(curl_str)
    heads = {}
    for item in header_arr:
        sub_arr = item.split(':', 1)
        if len(sub_arr) > 1:
            heads[sub_arr[0]] = sub_arr[1].strip()
    return heads


# 获取header值
def get_header_value(curl_str, key):
    mp = get_header_map(curl_str)
    return mp.get(key)


# 获取cookie字符串
def get_header_cookie_str(curl_str):
    headerMap = get_header_map(curl_str)
    cookie = headerMap.get('Cookie')
    if cookie == None:
        cookie = headerMap.get('cookie')
    return cookie


# 获取cookie内容
def get_cookie_dict(curl_str):
    cookiestr = get_header_cookie_str(curl_str)
    fields = cookiestr.split(';')
    # print(fields)

    dic = {}
    for f in fields:
        if f.find('=') > 0:
            key = f.split('=')[0].strip()
            dic[key] = f.split('=')[1].strip()

    # print(dic)
    return dic


# 获取post参数map
def get_param_map(curl_str):
    data_str = get_data_str(curl_str)
    arr = data_str.split('&')
    params = {}
    for param in arr:
        parr = param.split('=')
        if len(parr) > 1:
            params[parr[0]] = urllib.parse.unquote(parr[1])
    return params


# 用Request发出curl请求
def request_curl(curl_str):
    url = get_url(curl_str)
    # url = urllib.unquote(url)
    headers = get_header_map(curl_str)
    params = get_param_map(curl_str)
    if not params:
        params = get_data_binary_str(curl_str)

    if not params:
        params = get_data_raw_str(curl_str)

    # 如果还是没有参数，就发get请求
    if not params:
        gateway = url_util.get_url_gateway(url)
        params = url_util.get_url_params_map(url)
        urlparam = url_util.convert_dict_to_url_param(params)
        # return request_util.get(gateway+"?"+urlparam, params, headers)
        return request_util.get(gateway, params, headers)
    # print(url)
    # print(headers)
    # print(params)
    # log_util.loginfo("url: %s , headers: %s , params: %s", url, headers, params)

    return request_util.post(url, headers, params)


# 用Request发出curl请求
def request_download(curl_str, filepath):
    url = get_url(curl_str)
    # url = urllib.unquote(url)
    headers = get_header_map(curl_str)
    params = get_param_map(curl_str)
    if not params:
        params = get_data_binary_str(curl_str)

    # 如果还是没有参数，就发get请求
    if not params:
        gateway = url_util.get_url_gateway(url)
        params = url_util.get_url_params_map(url)
        return request_util.download(gateway, filepath, headers=headers, params=params)
    # print(url)
    # print(headers)
    # print(params)

    return request_util.download(url, filepath, headers=headers, params=params)


# 组装参数对
def build_headers_str(prefix, headers):
    arr = []
    for h in headers:
        str = "%s '%s'" % (prefix, h)
        arr.append(str)
    params_str = " ".join(arr)
    # print(params_str)
    return params_str


# 组装CURL字符串
def build_curl(url, headers, params):
    headers_str = build_headers_str('-H', headers)
    str_list = ['curl', "'%s'" % (url), headers_str, '--compressed']
    curl_str = " ".join(str_list)
    # print(curl_str)
    return curl_str


# 将参数值做urldecode
def urldecode_map_value(map={}):
    res = {}
    for k, v in map.items():
        # print(k, v)
        if isinstance(v, str):
            v = urllib.parse.unquote(v)
        res[k] = v
    return res


# 替换cookie
def replace_cookie(curl_str, cookie_new):
    cookie_new = replace_cookie_prefix(cookie_new)
    cookie_old = get_header_cookie_str(curl_str)
    return curl_str.replace(cookie_old, cookie_new)


# 替换data
def replace_data(curl_str, data_new):
    data_old = get_data_str(curl_str)
    if data_old == None or len(data_old.strip()) == 0:
        data_old = get_data_binary_str(curl_str)
    if data_old == None or len(data_old.strip()) == 0:
        data_old = get_data_raw_str(curl_str)
    return curl_str.replace(data_old, data_new)


def replace_cookie_prefix(cookie):
    cookie = cookie.replace("Cookie: ", "")
    cookie = cookie.replace("cookie: ", "")
    return cookie


# 替换机器地址，待http头
def replace_host(curl_str, host):
    chost = get_header_value(curl_str, 'Origin')
    curlstr = curl_str.replace(chost, host)
    return curlstr


# def replace_host(curl_str,)


if __name__ == '__main__':
    curl_str = '''
    curl 'http://icicada-zth-1.gz00b.stable.alipay.net/iworkbench/auto_name.json?_input_charset=utf-8&ctoken=SAf6vbiOqhtBGSs5&_ts=1583823348297' -H 'Connection: keep-alive' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'X-Requested-With: XMLHttpRequest' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Origin: http://icicada-zth-1.gz00b.stable.alipay.net' -H 'Referer: http://icicada-zth-1.gz00b.stable.alipay.net/iworkbench/VisitorCard.htm?appVersion=1.0001&loginEmail=youxi123_01@163.com' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'Cookie: JSESSIONID=2A292F2783B3230F3171B5AA87C04100; ; appExtInfo=%7B%22appVersion%22%3A%221.0001%22%2C%22appAlias%22%3A%22iworkbench%22%7D; BUSERVICE_TNTINSTID=ALIPW3SG; BUSERVICE_LAST_TNTINSTID=ALIPW3SG; zone=GZ00A; session.cookieNameId=ALIPAYBUMNGJSESSIONID; buservice_domain_id=KOUBEI_SALESCRM; SSO_EMPID_HASH_V2=17c3b8e74374497fc55cfc816bfb0afb; LOCALE=en_US; JSESSIONID=2A292F2783B3230F3171B5AA87C04100; route_group=LINKE_EI61574190_DFT_1070; ALIPAYIBUSERVICEJSESSIONID=GZ00F9012XD4fdWO0vXSngrex4TfWjipaybuserviceGZ00; ALIPAYBUMNGJSESSIONID=GZ00arb3Zwj5FtNXE2CW1yLf6VaX6yantbuserviceGZ00; ctoken=SAf6vbiOqhtBGSs5; BUSERVICE_SSO=4A21EF489ADA5128D2207262CB0CE6ED821817F331CA76B1C70F1779F4C59579; IAM_TOKEN=eyJraWQiOiJkZWZhdWx0IiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJjbmwiOiJCVUMiLCJzdWIiOiJqaW5sb25nLnJoaiIsImF1dGhfdHAiOlsiQ0VSVCIsIkRPTUFJTiJdLCJpc3MiOiJidW1uZy5zdGFibGUuYWxpcGF5Lm5ldCIsIm5vbmNlIjoiN2UxMzBlZmIiLCJzaWQiOiI5MDU0NCIsImF1ZCI6IioiLCJuYmYiOjE1ODM4MjMyODEsInNubyI6IjQwNDA2IiwidG50X2lkIjoiQUxJUFczQ04iLCJuYW1lIjoi6ZSm6b6ZIiwiZXhwIjoxNTgzOTA5NzQxLCJpYXQiOjE1ODM4MjMzNDEsImp0aSI6ImE3MGZmZWFmZjc5MDQ4MmVhZWI2MWNjODhjNzM0MmQyIn0.h-duunyJAbkyUNfs_ckMl_UOZYtgoMPd2akPetV_QrQ-ctgBZBCnSDmwzaJ3Umos5nsZAXIHILu5UNvT7-Wu8A' --data 'graphql=query%7BCrmMerchantQueryService_queryMerchantByLoginName_GraphQLString(arg0%3A%22youxi123_01%2540163.com%22)%7B*%7D%7D&appExtInfo=%7B%22appVersion%22%3A%221.0001%22%2C%22appName%22%3A%22iworkbench%22%2C%22appId%22%3A%221161901020000244043%22%2C%22tntInstId%22%3A%22ALIPW3SG%22%2C%22packageVersion%22%3A%228.0001%22%2C%22deployId%22%3A%221472003090000132225%22%2C%22appAlias%22%3A%22iworkbench%22%7D&uuid=83c2fd65-b7b4-44b6-bac2-f95d073ec15c' --compressed --insecure
    '''

    # convert_curl_to_array(curl_str)
    # print(get_param_map(curl_str))
    # print(get_header_map(curl_str))
    # url = get_url(curl_str)
    # print(url)

    # headers = get_headrs(curl_str)
    # params = get_param_map(curl_str)
    # build_headers_str('-H', headers)
    # build_curl(url, headers, params)
    # request_util.post(url, get_headrs(curl_str), get_param_map(curl_str))

    # curl_str = replace_cookie(curl_str, "xxxxxxxxxxxxxxxxxxxxxxxxxxx")
    # curl_str = replace_data(curl_str, "ccccccccccccccccccccccccccccc")
    # print(curl_str)
    # cookiestr = get_header_cookie_str(curl_str)
    # print(cookiestr)
    print(get_cookie_dict(curl_str))
