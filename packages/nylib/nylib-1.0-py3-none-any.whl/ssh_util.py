#!/usr/bin/python
# coding=utf-8
import paramiko, time


def ssh_connect(_host, _username, _password):
    _ssh_fd = paramiko.SSHClient()
    _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        _ssh_fd.connect(_host, username=_username, password=_password)
    except Exception as e:
        print('ssh %s@%s: %s' % (_username, _host, e))
        # exit()
    return _ssh_fd


def ssh_exec_cmd(_ssh_fd, _cmd, timeout=10, get_pty=True):
    return _ssh_fd.exec_command(_cmd, timeout, get_pty)


def ssh_close(_ssh_fd):
    _ssh_fd.close()


def remote_exec(hostname, username, password, cmd, timeout=10, get_pty=True):
    sshd = ssh_connect(hostname, username, password)
    try:
        stdin, stdout, stderr = ssh_exec_cmd(sshd, cmd, timeout, get_pty)
        stderr._set_mode('b')
        err_list = stderr.readlines()
        if len(err_list) > 0:
            print('ERROR:', err_list[0])
            # return ""

        str = ""

        for item in stdout.readlines():
            str = str + item
        ssh_close(sshd)
        return str
    except Exception as e:
        print('ERROR: ssh %s@%s: %s' % (username, hostname, e))


def paramiko_interact(hostname, username, password, cmd, do_with_rst):
    trans = paramiko.Transport((hostname, 22))  # 【坑1】 如果你使用 paramiko.SSHClient() cd后会回到连接的初始状态
    trans.start_client()
    # 用户名密码方式
    trans.auth_password(username, password)
    # 打开一个通道
    channel = trans.open_session()
    channel.settimeout(7200)
    # 获取一个终端
    channel.get_pty()
    # 激活器
    channel.invoke_shell()
    # cmd = 'cd /home/shell_study\r'
    # 发送要执行的命令
    # channel.send(cmd)
    # cmd = 'bash ./study_shell.sh\r' # 【坑2】 如果你使用 sh ./study_shell.sh\r 可能会出现 [: 11: y: unexpected operator 错误
    channel.send(cmd + '\n')
    # 回显很长的命令可能执行较久，通过循环分批次取回回显
    while True:
        time.sleep(0.2)
        rst = channel.recv(1024)
        try:
            rst = rst.decode('utf-8')
        except:
            rst = rst.decode('gbk')
        print(rst)
        # 通过命令执行提示符来判断命令是否执行完成
        # 【坑3】 如果你使用绝对路径，则会在home路径建立文件夹导致与预期不符
        code = do_with_rst(channel, rst)
        code = 0 if code == None else code
        if code < 0:
            break


    channel.close()
    trans.close()
    # channel.invoke_shell()


def scp_upload(hostname, username, password, localpath, remotepath, port=22):
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    # remotepath='/csdp/user_launcher-1.0-dev/user-1.0-release.jar'
    # localpath= r'D:\workspace\csdp201512041\csdp-ningxia\csdp_user\user\target\user-1.0-release.jar'
    sftp.put(localpath, remotepath)
    t.close()
    print("：） 成功上传 %s 文件。" % remotepath)


def scp_download(hostname, username, password, remotepath, localpath, port=22):
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    # remotepath='/csdp/user_launcher-1.0-dev/user-1.0-release.jar'
    # localpath= r'D:\workspace\csdp201512041\csdp-ningxia\csdp_user\user\target\user-1.0-release.jar'
    sftp.get(remotepath, localpath)
    t.close()
    print("：） 成功下载 %s 文件。" % localpath)


def main():
    hostname = 'icicada-zth-2.gz00b.stable.alipay.net'
    port = 22
    username = 'log'
    password = 'log_xixihaha'
    cmd = "grep --color=auto 89ef287b-5a56-4d8f-bded-8d6c4c9469db /home/admin/logs/tracelog/rpc-client-digest.log"

    ret = remote_exec(hostname, username, password, cmd)
    print(ret)


if __name__ == "__main__":
    main()
