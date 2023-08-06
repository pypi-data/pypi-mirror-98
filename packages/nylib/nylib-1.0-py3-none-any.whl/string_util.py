import string, re, json, uuid
import random, math
from python_utils import converters


def convert_to_int(str):
    return converters.to_int(str)


# 编码转换
def convert_utf8(str, charset):
    str = str.decode(charset).encode('utf-8')  # 以gbk编码格式读取g（因为他就是gbk编码的）并转换为utf-8格式输出
    return str


# 判断字符是否为中文
def is_zh(c):
    x = ord(c)
    # Punct & Radicals
    if x >= 0x2e80 and x <= 0x33ff:
        return True

        # Fullwidth Latin Characters
    elif x >= 0xff00 and x <= 0xffef:
        return True

        # CJK Unified Ideographs &
    # CJK Unified Ideographs Extension A
    elif x >= 0x4e00 and x <= 0x9fbb:
        return True
        # CJK Compatibility Ideographs
    elif x >= 0xf900 and x <= 0xfad9:
        return True

        # CJK Unified Ideographs Extension B
    elif x >= 0x20000 and x <= 0x2a6d6:
        return True

        # CJK Compatibility Supplement
    elif x >= 0x2f800 and x <= 0x2fa1d:
        return True

    else:
        return False


# 拆分中文和应为到两个数组中
def split_zh_en(zh_en_str):
    zh_en_group = []
    zh_gather = ""
    en_gather = ""
    zh_status = False
    mark = {"en": 1, "zh": 2}

    for c in zh_en_str:
        if not zh_status and is_zh(c):
            zh_status = True
            if en_gather != "":
                zh_en_group.append([mark["en"], en_gather])
                en_gather = ""
        elif not is_zh(c) and zh_status:
            zh_status = False
            if zh_gather != "":
                zh_en_group.append([mark["zh"], zh_gather])
        if zh_status:
            zh_gather += c
        else:
            en_gather += c
            zh_gather = ""

    if en_gather != "":
        zh_en_group.append([mark["en"], en_gather])
    elif zh_gather != "":
        zh_en_group.append([mark["zh"], zh_gather])

    return zh_en_group


# 下划线转驼峰
def underline_to_camel(underline_format):
    word_set = underline_format.split('_')
    if len(word_set) == 1:
        return underline_format

    camel_format = ''
    for i in range(len(word_set)):
        if i == 0:
            continue
        word_set[i] = word_set[i].capitalize()
    return ''.join(word_set)


@classmethod
def ltrim(cls, haystack, left=""):
    if cls.isEmpty(haystack):
        return haystack
    elif cls.isEmpty(left):
        return haystack.lstrip()
    else:
        return haystack.lstrip(left)


# 下划线转为驼峰格式
@classmethod
def camelize(cls, uncamelized, separator="_"):
    uncamelized = separator + uncamelized.lower().replace(separator, " ")
    return cls.ltrim(string.capwords(uncamelized).replace(" ", ""), separator)


# 驼峰转为下划线模式
@classmethod
def uncamelize(cls, camelCaps, separator="_"):
    pattern = re.compile(r'([A-Z]{1})')
    sub = re.sub(pattern, separator + r'\1', camelCaps).lower()
    return sub


# 拆分文本，每行处理,将每行结果合并为数组返回
def split_to_line(str, deal_line_func, *args):
    str = "" if str == None else str
    ret = []
    lines = str.splitlines(keepends=False)
    for line in lines:
        line = line.strip()
        if len(line.strip()) == 0:
            continue
        res = deal_line_func(line, *args)
        if res != None:
            ret.append(res)
    return ret


# 转成一行
def split_to_one_line(str):
    def _lamda(line):
        return line

    list = split_to_line(str, _lamda)
    return "".join(list)


# 匹配中间的字符串
def match_middle_str(str="", front="", behind=""):
    # str = '基金规模：59.29亿元（2019-03-31）'
    # front = '基金规模：'
    # behind = '亿元'
    # re.compile(r'')
    pt = eval("r'" + front + '(.*?)' + behind + "'")
    # print(pt)
    pattern = re.compile(pt)
    # pattern = re.compile(r'基金规模：(.*?)亿元')
    ret = pattern.findall(str)
    # print(ret)
    return ret


# 去掉头尾字符串
def cut_head_tail_str(str, head_str, tail_str):
    str = str.strip()
    if not str.startswith(head_str) or not str.endswith(tail_str):
        return str
    return str[len(head_str):-len(tail_str)]


# 加载jsonp数据
def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def get_uuid():
    return str(uuid.uuid4())


# 随机几位数
def rand_int(lengh=3):
    return random.randint(math.pow(10, lengh), math.pow(10, lengh + 1))


def rand_str(n=10):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, n))
    return ran_str


# 返回匹配到的IP数组
def match_ip(str):
    result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", str)
    if result:
        return result
    return []


# 过滤得到字符串中的数字
def filter_num(str):
    ret = re.findall("\d+", str)[0]
    # print(ret)
    return ret


def test():
    str = '''date_type时间类型
date_value时间值
group_id技能组
csat满意数
dsat不满意数
feedback_num总反馈数
csat_rate满意率:满意评价数/总留评量
csat_rate_compare_prev满意率环比
dsat_rate不满意率:不满意评价数/总留评量
dsat_rate_compare_prev不满意率环比
pickup_30_num30秒接起数
pickup_num总接起数
server_num服务总数
pickup_30_rate30秒接起率:30秒内对话的对话量/总访问量
pickup_30_compare_prev30秒接起率环比
pickup_rate接起率:对话量/总访问量
pickup_rate_compare_prev接起率环比
ht_total总对话时间
aht平均会话时间:总会话时间/总接起数
aht_compare_prev平均会话时间环比
'''

    res = split_zh_en(str)
    # print(res)
    flag = False
    for it in res:
        if it[0] == 1:
            print(it[1] + " STRING  COMMENT '", end='')
            flag = False
        if it[0] == 2:
            print(it[1] + "'")
            flag = True


if __name__ == '__main__':
    # test()
    # match_middle_str('', '', "")
    str = '2019-08-27 14:35:15,672 INFO  ZPROXY-RESPONSE-FINISH-DIGEST - [a8536c38-cdcd-403e-ae78-33ca0e993236,3e139f3e143cdaed9f47b42d807e8a6c,de833431e1978123729e521026f99cb2,tr,GZ00A,100.88.56.182,UTW,11.166.215.76,SofaRPC,com.alipay.mrchprod.common.service.facade.merchant.MrchProdClassificationMngFacade:1.0@DEFAULT,queryClassification,Y,SUCCESS,imif,mrchprod,1ms,11ms,11ms,5000ms,GEN>ZC]';
    str = '2019-08-27 06:35:15.593,imif,a8536c38-cdcd-403e-ae78-33ca0e993236,0.1.2.1,com.alipay.fc.fcbuservice.common.service.facade.OperatorFacade:1.0,queryByName,TR,SYNC,11.166.190.74:12200,ipaybuservice,UQX,,,,00,1027B,863B,3ms,0ms,0ms,3ms,SofaBizProcessor-4-thread-70,CFS,,F,,11.166.215.76,34604,GZ00A,F,,group4=LINKE_EI61466228_1428&tenantId=ALIPW3SG&abskey=999&group=LINKE_EI61466228_1428&FC_EVENT_CONTEXT={"operator":"jinlong.rhj"%2C"properties":{"BUSERVICE_REGION":"US"%2C"appVersion":""%2C"appName":"ipaycrm"%2C"appId":"1161707040000000101"%2C"tntInstId":"ALIPW3SG"%2C"packageVersion":"126.0002"%2C"deployId":""%2C"appAlias":"ipaycrm"}%2C"tntInstId":"ALIPW3SG"%2C"traceID":"a8536c38-cdcd-403e-ae78-33ca0e993236"}&';
    # print(match_ip(str))
    print(rand_int(2))
