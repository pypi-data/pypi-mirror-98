import functools
import asyncio
import threading
import sys, logging, os
import concurrent
from PyAsyncHelper3.core.Logging import Logging
from concurrent.futures import ThreadPoolExecutor


class Log(object):
    '''
    装饰器类
    '''

    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped_function(*args, **kwargs):
            self.notify()
            return func(*args, **kwargs)

        return wrapped_function

    def notify(self):
        print("当前线程{},当前进程{}".format(threading.current_thread(), os.getpid()))
        pass


import queue


class AsyncManager:
    __task_list = list()

    def __init__(self, main_loop, thread_number=500):
        """
        初始化
        @param main_loop: 主循环
        """
        self.main_loop = main_loop
        self.thread_loop = asyncio.new_event_loop()
        # 存储task的queue

        # 创建一个线程池
        self.thread_executor = ThreadPoolExecutor(thread_number)
        # 创建线程执行器
        # self.thread = concurrent.futures.Thraed()
        # 创建进程执行器
        # self.process = concurrent.futures.ProcessPoolExecutor()
        thread = threading.Thread(target=AsyncManager.thread_loop_func, args=(self.thread_loop,))
        thread.setDaemon(True)
        thread.start()

    @staticmethod
    def thread_loop_func(loop):
        '''
        :param loop: 事件loop对象
        :return: 无
        '''
        asyncio.set_event_loop(loop)
        loop.run_forever()

    @staticmethod
    async def task_check():
        while True:
            try:
                for task in AsyncManager.__task_list:
                    # 判断任务是否完成，完成则cacel()
                    if task.done():
                        task.cancel()
                        AsyncManager.__task_list.remove(task)
                #print("剩余task数量:{}".format(len(AsyncManager.__task_list)))
                await asyncio.sleep(2)
            except Exception as e:
                Logging.print(__file__, sys._getframe().f_lineno, sys._getframe().f_code.co_name, str(e))

    def add_task(self, func, args=None, callback=None, is_thread=True, is_process=False):
        """
        添加任务
        @param func: 函数
        @param args: 参数
        @param callback: 回调函数
        @param is_thread: 是否启动线程运行
        @param is_process:
        @return:
        """
        try:
            if not is_thread:
                # 添加async 异步函数,run_coroutine_threadsafe返回Future,无法await
                # new_loop = asyncio.new_event_loop()
                # 添加新的任务放入到线程循环中
                future = asyncio.run_coroutine_threadsafe(func, self.thread_loop)
                # 回调函数
                if callback:
                    future.add_done_callback(callback)
            else:
                # 不加async方法,并发执行,原理执行多个thread
                if args:
                    task = self.thread_loop.run_in_executor(self.thread_executor, func, *args)
                else:
                    task = self.thread_loop.run_in_executor(self.thread_executor, func)
                # # 回调函数
            AsyncManager.__task_list.append(task)
            return task
        except Exception as e:
            Logging.print(__file__, sys._getframe().f_lineno, sys._getframe().f_code.co_name, str(e))

    def loop_stop(self):
        self.thread_loop.stop()
        self.thread_loop.close()
