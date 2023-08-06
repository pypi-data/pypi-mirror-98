import time, functools, math, datetime, arrow

format_date_general = '%Y-%m-%d'
format_datetime_general = '%Y-%m-%d %H:%M:%S'


def getNowDateWithTimeZone():
    return arrow.now().format('YYYY-MM-DD HH:mm:ss ZZ')


def getCurDateStr():
    nowTime = time.localtime()
    year = str(nowTime.tm_year)
    month = str(nowTime.tm_mon)
    if len(month) < 2:
        month = '0' + month
    day = str(nowTime.tm_mday)
    if len(day) < 2:
        day = '0' + day
    return (year + '-' + month + '-' + day)


def getSimpleDateTimeStr():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# 获取10位长度的时间戳，精确到秒
def getTimestamps():
    return math.ceil(time.time())


# 将时间戳转换成时间,精确到秒
def convert_timestamp_to_date(timestamp, format='%Y-%m-%d %H:%M:%S'):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime(format, time_local)
    return dt


def convert_timestr_to_datetime(timestr, format='%Y-%m-%d %H:%M:%S'):
    # time_local = time.strptime(timestr, format)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    # dt = time.strftime(format, time_local)

    # 转为时间数组，分别利用time模块和datetime模块
    # timeArray = time.strptime(timestr, format)
    # print(timeArray)

    datetimeArray = datetime.datetime.strptime(timestr, format)

    return datetimeArray


# 将datetime对象转为字符串
def datetime_to_str(date=None, format='%Y-%m-%d %H:%M:%S'):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(format)


def convert_to_timezone(dt=datetime.datetime.utcnow(), timezone_hour=8):
    print(dt)
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    print(dt)
    tzutc = datetime.timezone(datetime.timedelta(hours=timezone_hour))
    local_dt = dt.astimezone(tzutc)
    print(local_dt)
    print(local_dt.strftime('%Y-%m-%d %H:%M:%S%z'))

    return local_dt


def add_day(start, n):
    # start = datetime.datetime.now()
    date = start + datetime.timedelta(days=n)
    return date


def add_hour(start, n):
    date = start + datetime.timedelta(hours=n)
    return date


def add_seconds(start, n):
    date = start + datetime.timedelta(seconds=n)
    return date


def timestr2sec(x):
    x = "00:00:" + x if len(x.split(':')) < 2 else x
    x = "00:" + x if len(x.split(':')) < 3 else x
    '''
    字符串时分秒转换成秒
    '''
    h, m, s = x.strip().split(':')  # .split()函数将其通过':'分隔开，.strip()函数用来除去空格
    return int(h) * 3600 + int(m) * 60 + int(s)  # int()函数转换成整数运算


def time2sec(y):
    '''
    时间类型时分秒转换成秒
    '''
    h = y.hour  # 直接用datetime.time模块内置的方法，得到时、分、秒
    m = y.minute
    s = y.second
    return int(h) * 3600 + int(m) * 60 + int(s)  # int()函数转换成整数运算


# 统计方法执行耗时
# @time_cost("cost")
# def test2(x):
#     time.sleep(0.2)
def time_cost(info="used"):
    def _time_cost(fn):
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            start = time.time()
            fn(*args, **kwargs)
            # print(time.time() - start)
            print("%s %s %s" % (fn.__name__, info, time.time() - start), "second")

        return _wrapper

    return _time_cost


class TimeCost(object):
    def __init__(self):
        pass

    def __call__(self, fn):
        def _call(*args, **kw):
            start = time.time()
            fn(*args, **kw)
            print("%s %s" % (fn.__name__, time.time() - start), "second")

        return _call


@time_cost()
def test(x, y):
    time.sleep(3)


@time_cost("cost")
def test2(x):
    time.sleep(1)


def sleep(secends):
    time.sleep(secends)


def countdown(secends):
    for i in range(secends, 0, -1):
        print("\r", "Please Wait: {}s".format(i), end="", flush=True)
        time.sleep(1)
    print("\r", "Please Wait: {}s".format(0), end="", flush=True)
    print()


if __name__ == '__main__':
    # test(1, 2)
    # test2(2)
    # print(getSimpleDateTimeStr())
    # print(getTimestamps())
    # print(convert_timestr_to_datetime('2015-05-27', format_date_general))
    # print(datetime.datetime.now())
    # convert_to_timezone()
    countdown(5)
