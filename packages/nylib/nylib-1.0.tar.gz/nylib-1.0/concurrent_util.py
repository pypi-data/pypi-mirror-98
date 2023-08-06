import threading, logging
import multiprocessing
from multiprocessing import cpu_count
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor, wait
from . import date_util


def getDefaultThreadPool(workers=cpu_count() * 2):
    if workers <= 0:
        workers = cpu_count() * 2
    return ThreadPoolExecutor(max_workers=workers)


def getDefaultProcessPoll(workers=cpu_count()):
    if workers <= 0:
        workers = cpu_count()
    pool = multiprocessing.Pool(workers)
    return pool


# 指定执行次数,没有参数，不关心结果
def threadPoolExecute(task_func, run_times=0, workers=0):
    pool = getDefaultThreadPool(workers)
    for i in range(0, run_times):
        pool.submit(task_func)  # 往线程池里面加入一个task


# 带参数列表异步执行,不阻塞主线程
# task_func函数处理单条，接收params中的单个参数
def threadPoolExecuteWithParams(task_func, params=[], workers=0):
    pool = getDefaultThreadPool(workers)
    for param in params:
        pool.submit(task_func, param)


# 同步返回与提交参数顺序一致的结果迭代器，调用方自己遍历处理
def threadPoolExecuteReturn(task_func, params=[], workers=0):
    pool = getDefaultThreadPool(workers)
    res_iter = pool.map(task_func, params)
    # for res in res_iter:
    #     print("ret: ", res)
    return res_iter


# 阻塞模式，等待调用完成，返回无序map
def threadPoolExecuteSyncReturn(task_func, params=[], timeout=None, workers=0):
    pool = getDefaultThreadPool(workers)

    mp = dict()
    ret = dict()

    for param in params:
        future = pool.submit(task_func, param)
        mp[future] = param

    for future in futures.as_completed(mp):
        param = mp[future]
        try:
            data = future.result()
            ret[param] = data
        except Exception as exc:
            logging.exception(exc)
            print(exc, ',param:', param)
        else:
            # print('param:', param)
            None

    return ret


# 调用方阻塞，等待处理,params是需要遍历的参数列表,如果函数需要多个参数， 需要自行封装成一个参数
def threadPoolExecuteSync(task_func, params=[], timeout=None, workers=0, show_progress=False):
    pool = getDefaultThreadPool(workers)

    i = 0
    future_tasks = [pool.submit(task_func, param) for param in params]
    try:
        result = wait(future_tasks, timeout=timeout, return_when=futures.ALL_COMPLETED)

        done_set = result[0]
        undone_set = result[1]
        for future in done_set:
            i = i + 1
            if show_progress:
                print('progress: %s/%s' % (i, len(params)))
            data = future.result()
            # print('第一个网页任务完成 url:%s , len:%d bytes! ' % (resp.url, len(resp.text)))
    except Exception as e:
        print('exception :', e)
        logging.exception(e)
    finally:
        pass


# 非阻塞，异步调用，回调模式，future会传给回调函数
def threadPoolExecuteWithCallback(task_func, params=[], callback_func=None, workers=0):
    pool = getDefaultThreadPool(workers)
    mp = dict()
    ret = dict()
    for param in params:
        future = pool.submit(task_func, param)
        mp[future] = param
        future.add_done_callback(callback_func)

        # for future in futures.as_completed(mp):
        #     param = mp[future]
        #     try:
        #         data = future.result()
        #         ret[param] = data
        #     except Exception as exc:
        #         print(exc, ',param:', param)
        #     else:
        #         # print('param:', param)
        #         None
        #
        # return ret


def processPoolExecuteAsync(task_func, params=[], workers=0):
    pool = getDefaultProcessPoll(workers)

    for param in params:
        pool.apply_async(task_func, (param))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去


def processPoolExecuteSync(task_func, params=[], workers=0):
    pool = getDefaultProcessPoll(workers)

    for param in params:
        pool.apply(task_func, (param,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    pool.close()  # 关闭进程池，表示不能在往进程池中添加进程
    pool.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用


# 获取当前线程id
def getCurrentThreadId():
    return threading.currentThread().ident


# 异步执行注解
def async_run(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


# 本地并发锁
lock = {}


# 超时锁，判断是否超时，key用于区分不同业务，timeout单位是秒
def lock_timeout(key, timeout=60):
    global lock
    lockdate = lock.get(key, None)
    if not lockdate:
        lock[key] = date_util.getTimestamps() - timeout

    if (date_util.getTimestamps() - lock[key]) > timeout:
        lock[key] = date_util.getTimestamps()
        return True
    return False


counter = {}


# 计数器初始化
def counter_init(key):
    global counter
    counter[key] = 0


# 计数器累加
def counter_accumulate(key, print=False):
    global counter
    curr = counter.get(key, 0)
    counter[key] = curr + 1
    if print:
        info = 'counter key: %s , current: %d' % (key, counter[key])
        logging.info(info)
    return counter[key]


def func(msg):
    print(multiprocessing.current_process().name + '-' + msg)


if __name__ == '__main__':
    processPoolExecuteSync(func, range(1, 10))
