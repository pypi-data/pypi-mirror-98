import os

from croniter import croniter
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


def interval(func, seconds):
    sched.add_job(func, 'interval', seconds=seconds)
    sched.start()


# def cron(func):
#     sched.add_job(func, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
#     sched.start()
# 返回cron表达式的下次执行时间，表达式规则：分时日月周秒
def next_process_time(cron_str):
    iter = croniter(cron_str, datetime.now())

    iter.get_next(datetime)
    # print(iter.get_next(datetime))
    # print(iter.get_current(datetime))
    # print(type(iter.get_current(datetime)))
    # 打印结果为：2019-02-22 08:00:00
    return iter.get_current(datetime)


# 到下次执行时间的剩余秒数
def next_remaining_seconds(cron_str):
    datetime = next_process_time(cron_str)
    now = datetime.now()
    diff = datetime - now
    return diff.seconds


# 下次执行时间，小于约定时间，则触发
def is_trigger_now(cron_str, diff_seconds=60):
    diff = next_remaining_seconds(cron_str)
    if abs(diff) < diff_seconds:
        return True
    return False


if __name__ == '__main__':
    # next_time("0 8 * * *")
    print(next_process_time("1 * * * *"))
    print(next_remaining_seconds("1 10/12 * * *"))
    print(is_trigger_now("1 10/12 * * *"))
