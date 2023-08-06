# async4s - 一个简单易用的异步执行模块

## About
这是一个简单易用的异步执行模块，提供几个python装饰器，使原有方法轻松变为异步执行。  

## Requirements
- Python3

## Install
通过pip命令安装：
```shell
pip install async4s
```

## Example
```python
import time

import async4s

# Use 4 threads.
pool = async4s.ThreadPool(max_workers=4)

@async4s.task(pool)
def work():
    time.sleep(3)
    return "Work Done!!!"

@async4s.callback(pool)
def work_callback(work):
    print(work.result())


for i in range(4):
    work()
pool.shutdown()
print("All done")
```

## Release History
### 0.0.1(2021-01-26)
- Birth

## Author
- <a href="mailto:pmq2008@gmail.com">Rocky Peng</a>
