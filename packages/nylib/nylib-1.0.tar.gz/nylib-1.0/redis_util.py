# coding:utf-8
import time
import redis

import json
import types
import collections
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class redisClient():
    def __init__(self, **kwargs):
        """
        init topic object
        :param kwargs:
        """
        super().__init__()
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.db = kwargs.get('db')
        self.password = kwargs.get('password')
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)
        r = redis.Redis(connection_pool=self.pool)
        r.execute_command('config set notify-keyspace-events KEA')  # 发布端，判断如果是第一次就执行

    def pub(self, channel, message):
        rc = redis.StrictRedis(connection_pool=self.pool)
        rc.publish(channel, message)  # 发布消息到liao

    def getRedis(self):
        rc = redis.StrictRedis(connection_pool=self.pool)
        return rc

    # def sub(self):
    #     rc = redis.StrictRedis(connection_pool=self.pool)
    #     ps = rc.pubsub()
    #     ps.subscribe('liao')  # 从liao订阅消息
    #     for item in ps.listen():  # 监听状态：有消息发布了就拿过来
    #         if item['type'] == 'message':
    #             print(item['channel'])
    #
    #             print(item['data'])


    def regeist_handler(self, channel, handler):
        if channel not in self.registed_handler_dic:
            self.channel_lst.append(channel)

        self.registed_handler_dic[channel].append(handler)


class PubSubSever(object):
    """
    发布订阅服务器， 使用 非阻塞的方式+ 进程池实现， 为每个channel的handler 开辟一个进程
    """

    def __init__(self, redis_conn_pool, channel_lst=[], max_worker_num=10, pool_type='thread'):
        self.rcon = redis.StrictRedis(connection_pool=redis_conn_pool)
        # 初始化线程池
        self.process_pool = ProcessPoolExecutor(max_worker_num) if pool_type == 'proc' else ThreadPoolExecutor(
            max_worker_num)
        self.channel_lst = channel_lst
        self.registed_handler_dic = collections.defaultdict(list)
        self.pubsub = self.rcon.pubsub()

    def init_sub(self):
        self.pubsub.subscribe(*self.channel_lst)

    def regist_handler(self, channel, handler):

        if channel not in self.registed_handler_dic:
            print("regist_handler, channel:", channel, ", hander:", handler)
            if '*' in str(channel):
                # 同时订阅多个频道，要用psubscribe
                self.pubsub.psubscribe(channel)
            else:
                self.pubsub.subscribe(channel)
            self.channel_lst.append(channel)

        self.registed_handler_dic[channel].append(handler)

    def decode_message(self, message):
        return json.loads(message)

    def parse_message(self, message):
        msg = self.decode_message(message)
        return msg['channel'], msg['data']

    def notify(self, channel, data):
        channel = channel.decode('utf-8')
        idx = 0
        for handler in self.registed_handler_dic[channel]:
            # print(channel, handler)
            if isinstance(handler, types.FunctionType) or hasattr(handler, '__call__'):
                # print("取出handle")
                # 将handler 和数据封装到一个进程任务中
                self.process_pool.submit(handler, data)

    def event_loop(self):
        """
        服务器以非阻塞的方式运行
        :return:
        """
        while True:
            item = self.pubsub.get_message()  # 非阻塞方式
            # for item in self.pubsub.listen():     # 阻塞方式开启循环
            # print("get_message item: ", item)
            time.sleep(1)
            if not item:
                continue
            if item['type'] == 'message':
                print("event_loop: ", item)
                # channel,data = self.parse_message(item)
                channel, data = item['channel'], item['data']
                self.notify(channel, data)
                # time.sleep(1)
            if item['type'] == 'pmessage':
                pattern, channel, data = item['pattern'], item['channel'], item['data']
                # 如果是过期消息，就将key返回个handler处理
                if data == bytes('expired', encoding="utf8"):
                    key = str(channel).split(":")[1]
                    self.notify(pattern, key)

    def close(self):
        self.pubsub.close()
        self.rcon.reset()
        self.process_pool.shutdown()


if __name__ == '__main__':
    redisClient = redisClient(host="t.navyran.top", port=6399, db=1, password="Jinlong1234")
    # redisClient.sub()
    # redisClient.pub()

    # p.unsubscribe('spub')
    redisClient.pub("channel1", "haha")
