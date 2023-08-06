import requests, json
from pylib import url_util, object_util


def default_session():
    session = requests.Session()
    # print(1)
    # session.headers.update({'Cookie': 'JSESSIONID=083B61FCADA4DB211F33FDBE28B6F7DC; _gscu_1276227783=33815256qcspdf21; route=9822522b30f663ac278178ba378ac6d4'})
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})
    return session


def build_session(heads={}):
    session = requests.Session()
    if any(heads):
        session.headers.update(heads)
    else:
        session = default_session()
    return session


# 解析url中的参数请求
def getFromUrl(url):
    u = url_util.get_url_gateway(url)
    p = url_util.get_url_params_map(url)
    ret = get(u, p)
    return ret


# 发送get请求，网关与参数要分开
def get(url, params={}, headers=None, payload=None, proxies={}, timeout=60):
    # session = default_session()
    # ret1 = session.get(url)
    # print(proxies)
    ret1 = requests.get(url, params, headers=headers, proxies=proxies, timeout=timeout, verify=False)
    return ret1


# 发送post请求
def post(url, headers=None, payload=None, proxies={}):
    # print(url)
    # print(headers)
    # print(payload)
    # session = build_session(headers)
    if object_util.typeof(payload) == 'str':
        payload = payload.encode("utf-8")
    elif object_util.typeof(payload) == 'dict':
        payload = json.loads(json.dumps(payload).encode('utf-8'))
    ret = requests.post(url, headers=headers, data=payload, proxies=proxies, verify=False)
    # print(ret)
    # print(ret.text)
    return ret


def post_json(url, json={}):
    return requests.post(url=url, json=json)


# 文件下载
def download(url, down_path, params={}, headers=None, payload=None, proxies={}, verify=True):
    r = requests.get(url, params, headers=headers, proxies=proxies, verify=verify)
    with open(down_path, "wb") as code:
        code.write(r.content)


# 转换返回内容的编码
def convert_res_charset(res, charset):
    return res.text.encode(res.encoding).decode(charset)


def get_json(url, params={}, headers=None, payload=None):
    ret = get(url, params, headers, payload)

    ret_json = {}
    if len(ret.text) > 0:
        ret_json = json.loads(ret.text)
    return ret_json


def get_proxies_param(proxyserver, proxyport):
    proxy = '%s:%s' % (proxyserver, proxyport)
    proxies = {
        'http': 'socks5://' + proxy,
        'https': 'socks5://' + proxy,
    }
    return proxies


if __name__ == '__main__':
    resp = get("https://www.facebook.com/", proxies=get_proxies_param('navyran.top', 38989))
    print(resp.text)
