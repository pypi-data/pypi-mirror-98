from urllib.parse import urlparse, quote, unquote


# 获取url问号前面的网关地址
def get_url_gateway(url):
    arr = url.split("?")
    # print(arr[0])
    return arr[0]


# 获取url中的参数对
def get_url_params_map(url):
    arr = url.split("?")
    if len(arr) < 2:
        return {}
    paramstr = arr[1]
    parr = paramstr.split("&")
    # print(parr)
    map = {}
    for str in parr:
        kvarr = str.split("=")
        # print(kvarr)
        if len(kvarr) == 2:
            map[kvarr[0]] = kvarr[1]
    # print(map)
    return map


def get_host(url):
    urlgroup = urlparse(url)
    return urlgroup.scheme + '://' + urlgroup.hostname


def urlencode(str):
    return quote(str, 'utf-8')


def urldecode(str):
    return unquote(str, 'utf-8')


# 将字典转为url参数
def convert_dict_to_url_param(dict={}):
    lst = []
    for (k, v) in dict.items():
        v = str(v)
        lst.append("%s=%s" % (k, urlencode(v)))
    return "&".join(lst)


# 将url参数转为字典
def convert_url_param_to_dict(paramstr=''):
    dict = {}
    arr = paramstr.split('&')
    for item in arr:
        # print(item)
        arr2 = item.split('=')
        if len(arr) > 0:
            dict[arr2[0]] = urldecode(arr2[1])
    return dict


if __name__ == '__main__':
    paramstr = '_input_charset=utf-8&ctoken=6hRNQPoKflJdUxqO&start=0&limit=20&pageIndex=1&resourceType=BLOCK&appName=&orgId=&securityLevel=&optCode=FUNC_CRM_MERCHANT_SITE_QUERY&resInfo=&optCodeDesc=&url='
    print(convert_url_param_to_dict(paramstr))
