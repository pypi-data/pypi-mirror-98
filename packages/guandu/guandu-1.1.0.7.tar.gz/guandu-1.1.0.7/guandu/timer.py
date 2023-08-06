# encoding: utf-8

import time


def localtime_to_str() -> str:
    """
    获取当前时间的%Y-%m-%d %H:%M:%S格式
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


if __name__ == '__main__':
    print(localtime_to_str())
