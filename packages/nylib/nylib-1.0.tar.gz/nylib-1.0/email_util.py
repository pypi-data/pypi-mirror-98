import yagmail
from .concurrent_util import async_run


def send_mail(receivers, subject="", content="", files=[]):
    # 链接邮箱服务器
    yag = yagmail.SMTP(user="kbtest@aliyun.com", password="Kbtestjinlong1234", host='smtp.aliyun.com')
    # 邮箱正文
    contents = ['This is the body, and here is just text http://somedomain/image.png',
                'You can find an audio file attached.', '/local/path/song.mp3']
    # 发送邮件
    yag.send(receivers, subject, content, attachments=files)


@async_run
def send_mail_async(receivers, subject="", content="", files=[]):
    send_mail(receivers, subject, content, files)


if __name__ == '__main__':
    send_mail('ranhaijun1129@163.com', "a", 'b', files=['/Users/jinlong.rhj/Downloads/gotty_darwin_amd64.tar.gz'])
