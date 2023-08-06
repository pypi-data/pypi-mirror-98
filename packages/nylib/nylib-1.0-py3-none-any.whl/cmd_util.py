# coding=utf-8
'''
Created on 2013年11月22日

@author: crazyant.net
'''
import shlex, os
import datetime
import subprocess
import time
import sh


def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """执行一个SHELL命令
            封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
           参数:
        cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    Returns: return_code
    Raises:  Exception: 执行超时
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)

    sub = subprocess_popen_param_array(cmdstring_list, cwd, shell, timeout)

    return (str(sub.returncode), str(sub.stdout), str(sub.stderr))


# 传数组参数，执行返回
def subprocess_popen_param_array(cmdstring_list, cwd=None, shell=False, timeout=None):
    # 没有指定标准输出和错误输出的管道，因此会打印到屏幕上；
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, shell=shell,
                           bufsize=4096)
    # subprocess.poll()方法：检查子进程是否结束了，如果结束了，设定并返回码，放在subprocess.returncode变量中

    end_time = datetime.datetime.now() + datetime.timedelta(days=1)

    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % ' '.join(cmdstring_list))
    # for i in iter(sub.stdout.readline, 'b'):
    #     print(i)
    return sub


def exec_shell(shellstr, charset='utf8'):
    # curl = "curl -H 'Host: zt.wps.cn' -H 'Content-Type: application/json' -H 'Accept: */*' -H 'sid: V02SffcFNB9nA58U3Yx2U_KpyN0dHS400a8c765300001ad274' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN' -H 'Referer: https://servicewechat.com/wx2f333d84a103825d/42/page-frame.html' -H 'Accept-Language: zh-cn' --compressed 'https://zt.wps.cn/2018/clock_in/api/get_question?member=wps'"
    sub = subprocess.Popen(shellstr, cwd=None, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           shell=True,
                           bufsize=4096)
    sub.wait()
    # for i in iter(sub.stdout.readline,'b'):
    #     print(i)
    bstr = sub.stdout.read()
    if bstr:
        return bstr.decode(charset)
    return ''
    # print(sub.stdout.read().decode('utf-8'))
    # print(sub.stderr.readlines())


def test2():
    data = ['www.baidu.com',
            'www.csdn.cn']

    for item in data:
        tmpres = os.popen('curl %s' % item).readlines()
        print(tmpres)


def sh_test():
    print(sh.ifconfig("eth0"))
    print(sh.google_chrome("http://google.com"))


if __name__ == "__main__":
    # print(execute_command("ls"))
    # import sys
    #
    # defaultencoding = 'utf-8'
    # if sys.getdefaultencoding() != defaultencoding:
    #     os.reload(sys)
    #     sys.setdefaultencoding(defaultencoding)
    # test2()
    # test3()
    sh_test()

