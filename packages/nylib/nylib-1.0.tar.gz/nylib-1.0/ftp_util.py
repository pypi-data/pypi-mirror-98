import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP


 # '''
# #用户名     密码       权限         目录
## root      12345      elradfmwM    /home/
# huangxm     12345      elradfmwM    /home/
# test       12345      elradfmwM    /home/huangxm
# '''
def get_user(userfile):
    #定义一个用户列表
    user_list = []
    with open(userfile) as f:
        for line in f:
            if not line.startswith('#') and line:
                if len(line.split()) == 4:
                    user_list.append(line.split())
                else:
                    print("user.conf配置错误")
    return user_list

def ftp_server():
    # 实例化用户授权管理
    authorizer = DummyAuthorizer()
    # authorizer.add_user('user', '12345', dir_path, perm='elradfmwMT')  # 添加用户 参数:username,password,允许的路径,权限

    # user_list = get_user('conf/user.py')
    # for user in user_list:
    #     name, passwd, permit, homedir = user
    #     try:
    #         authorizer.add_user(name, passwd, homedir, perm=permit)
    #     except Exception as e:
    #         print(e)

    authorizer.add_anonymous(os.getcwd())  # 这里是允许匿名用户,如果不允许删掉此行即可

    # 实例化FTPHandler
    handler = FTPHandler
    handler.authorizer = authorizer

    # 设定一个客户端链接时的标语
    handler.banner = "pyftpdlib based ftpd ready."


    # handler.masquerade_address = '151.25.42.11'#指定伪装ip地址
    handler.passive_ports = range(60000, 65535)#指定允许的端口范围

    address = ("localhost", 2121)  # FTP一般使用21,20端口
    server = FTPServer(address, handler)  # FTP服务器实例

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # 开启服务器
    server.serve_forever()


def ftp_client():
    ftp = FTP()
    ftp.connect('localhost', 21)  # localhost改成服务器ip地址
    ftp.login(user='user', passwd='12345')

    file = open('f://ftpdownload/test.txt', 'wb')
    ftp.retrbinary("RETR test.txt", file.write, 1024)  # 从服务器上下载文件 1024字节一个块
    ftp.set_debuglevel(0)
    ftp.close()

if __name__ == '__main__':
    ftp_server()