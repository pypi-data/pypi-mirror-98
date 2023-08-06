import time
from pytz import utc
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import functools

import redis  # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库

blockingScheduler = BlockingScheduler()
backgroundScheduler = BackgroundScheduler()

scheduler = None

# pool = redis.ConnectionPool(
#     host='docker-jl.dockerlab.alipay.net',
#     port=6379,
#     password='redisjinlong'
# )
# rds = redis.StrictRedis(connection_pool=pool)

jobstores = {
    'redis': RedisJobStore(2, host='docker-jl.dockerlab.alipay.net',
                           port=6379,
                           password='redisjinlong'),
    'mongo': MongoDBJobStore(
        host='mongodb://test:testjinlong@mongo-jl.dockerlab.alipay.net:27017/apscheduler?authMechanism=SCRAM-SHA-1&authSource=apscheduler',
        port=27017, ),
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {

    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {

    'coalesce': False,
    'max_instances': 3
}


def initScheduler(init_scheduler=None):
    global scheduler
    if init_scheduler != None:
        scheduler = init_scheduler
        return scheduler
    else:
        scheduler = blockingScheduler

    return scheduler


# 常规阻塞间隔执行，单位为秒
def run_blocking_scheduler_interval(job_func, seconds):
    scheduler = initScheduler()
    job = scheduler.add_job(job_func, 'interval', seconds=seconds)
    scheduler.start()


# def run_blocking_scheduler_datetime(job_func,datetime):


def redis_scheduler_interval(job_func, seconds):
    scheduler = initScheduler()
    scheduler.add_jobstore('redis', jobs_key='example.jobs', run_times_key='example.run_times')
    scheduler.start()


# 直接运行的方法
def run_scheduler_cron(job_func, cron):
    scheduler = initScheduler()
    # print(scheduler)
    # sched.add_job(job_function, CronTrigger.from_crontab('0 0 1-15 may-aug *'))
    job = scheduler.add_job(job_func, CronTrigger.from_crontab(cron))
    scheduler.start()


def run_pool():
    backgroundScheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
                                              timezone=utc)
    scheduler = initScheduler(backgroundScheduler)
    job = scheduler.add_job(job_func, trigger='interval', seconds=2, jobstore='redis', id='aaac')
    scheduler.start()
    return scheduler


# cron运行装饰器, 被装饰的方法不能有入参
def run_cron_decorator(cron):
    '''定时任务装饰器'''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                run_scheduler_cron(func, cron)
            except Exception as e:
                print(e)
                pass

        return wrapper

    return decorator


# 间隔运行装饰器, 被装饰的方法不能有入参
def run_interval(interval_seconds=10):
    '''定时任务装饰器'''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                run_blocking_scheduler_interval(func, interval_seconds)
            except Exception as e:
                print(e)
                pass

        return wrapper

    return decorator


def evaluate(expression):
    '''
    order of values
    year, month, day, week, day_of_week, hour, minute, second, start_date, end_date, timezone
    '''
    splitValues = expression.split()
    for i in range(0, 8):
        if (i == 0):
            if (splitValues[0] == '?'):
                year = None
            else:
                year = splitValues[0]
        if (i == 1):
            if (splitValues[1] == '?'):
                month = None
            else:
                month = splitValues[1]
        if (i == 2):
            if (splitValues[2] == '?'):
                day = None
            else:
                day = splitValues[2]
        if (i == 3):
            if (splitValues[3] == '?'):
                week = None
            else:
                week = splitValues[3]
        if (i == 4):
            if (splitValues[4] == '?'):
                day_of_week = None
            else:
                day_of_week = splitValues[4]
        if (i == 5):
            if (splitValues[5] == '?'):
                hour = None
            else:
                hour = splitValues[5]
        if (i == 6):
            if (splitValues[6] == '?'):
                minute = None
            else:
                minute = splitValues[6]
        if (i == 7):
            if (splitValues[7] == '?'):
                second = None
            else:
                second = splitValues[7]
    return year, month, day, week, day_of_week, hour, minute, second


def getTrigger(cronExpression):
    year, month, day, week, day_of_week, hour, minute, second = evaluate(cronExpression)
    trigger = CronTrigger(year, month, day, week, day_of_week, hour, minute, second)
    return trigger


def job_func():
    print(111)


@run_cron_decorator('*/1 * * * *')
def job_func2():
    print(111)


if __name__ == '__main__':
    # redis_scheduler_interval(job_func, 10)
    # test_redis()
    # scheduler = run_pool()
    # time.sleep(10)
    # scheduler.remove_job('aaac', 'redis')
    run_blocking_scheduler_interval(job_func, 1)
    cron = '*/1 * * * *'
    # print(getTrigger(cron))
    # run_scheduler_cron(job_func, cron)
    # job_func2()
