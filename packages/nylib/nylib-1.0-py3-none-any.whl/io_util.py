import sys


class StringBuffer(object):
    def __init__(self):
        self.buffer = []

    def write(self, *args, **kwargs):
        self.buffer.append(args)


# 将函数的标准输出内容拦截并返回
def stdout_intercept_wrapper(func, *args, **kwargs):
    stdout = sys.stdout
    sys.stdout = StringBuffer()

    func(*args, **kwargs)

    sb, sys.stdout = sys.stdout, stdout
    # print(sb.buffer)
    ret = ""
    for item in sb.buffer:
        # print(item[0],end='')
        ret += item[0]
    # print(''.join(sb.buffer))
    return ret
