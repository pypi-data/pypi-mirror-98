from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, as_completed


# 不要求返回结果
def threadPoolExecutor(pool_size, task_func, params):
    pool = ThreadPoolExecutor(max_workers=pool_size)  # 创建一个最大可容纳2个task的线程池

    for i in range(pool_size):
        # print(task_func)
        if params:
            future = pool.submit(task_func, params)  # 往线程池里面加入一个task
        else:
            future = pool.submit(task_func)

            # print(future.done())  # 判断task1是否结束
            # time.sleep(3)


            # print(future1.result())  # 查看task1返回的结果


# 不要求返回结果
def processPoolExecutor(pool_size, task_func, params):
    pool = ProcessPoolExecutor(max_workers=pool_size)  # 创建一个最大可容纳2个task的线程池

    for i in range(pool_size):
        # print(task_func)
        if params:
            future = pool.submit(task_func, params)  # 往线程池里面加入一个task
        else:
            future = pool.submit(task_func)


# 等待线程池执行完成，返回futures
def waitThreadPoolExecute(pool_size, task_func, params):
    pool = ThreadPoolExecutor(pool_size)
    futures = []
    for x in range(pool_size):
        future = pool.submit(task_func, params)
        futures.append(future)

    return wait(futures)
