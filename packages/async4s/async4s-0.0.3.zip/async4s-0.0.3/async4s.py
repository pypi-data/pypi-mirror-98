#!/usr/bin/env python

import multiprocessing
from concurrent.futures import ThreadPoolExecutor


class ThreadPool:
    def __init__(self, max_workers=None):
        if max_workers is None:
            self.max_workers = multiprocessing.cpu_count()
        else:
            self.max_workers = max_workers
        self.pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.callbacks = []
        self.results = []

    def submit(self, f, *args, **kwargs):
        self.pool._adjust_thread_count()
        task = self.pool.submit(f, *args, **kwargs)
        self.results.append(task)
        return task

    def shutdown(self, wait=True):
        self.pool.shutdown(wait)


def task(pool):
    def _task(f):
        def do_task(*args, **kwargs):
            result = pool.submit(f, *args, **kwargs)
            for cb in pool.callbacks:
                result.add_done_callback(cb)
            return result

        return do_task

    return _task


def callback(pool):
    def _callback(f):
        pool.callbacks.append(f)

        def register_callback():
            f()

        return register_callback

    return _callback
