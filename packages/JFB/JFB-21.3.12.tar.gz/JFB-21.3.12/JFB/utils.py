# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       utils
   Description :
   Author:          蒋付帮
   date:            2019-10-28 16:32
-------------------------------------------------
   Change Activity:
                    2021-03-12: 代码优化/功能更新
-------------------------------------------------
"""
__author__ = 'jiangfb'

import datetime
import math


def headers_str_to_dict(headers_str: str) -> dict:
    """
    :param headers_str: headers字符串格式
    :return: headers字典格式
    headers字符串格式转字典格式
    """
    lines = headers_str.split("\n")
    headers = dict()
    for line in lines:
        if line.strip():
            key, value = line.split(": ")
            headers[key.strip()] = value.strip()
    return headers

def timestamp_to_datetime(timestamp) -> datetime:
    """
    :param timestamp: 字符串或整形型时间戳(10/13位均可)
    :return: local-datetime类型
    时间戳转datetime类型
    """
    if isinstance(timestamp, str):
        if len(timestamp) == 13:
            timestamp = int(timestamp[:-3])
        else:
            timestamp = int(timestamp)
    elif isinstance(timestamp, int):
        if len_int(timestamp) == 13:
            timestamp = timestamp / 1000
    timeArray = datetime.datetime.fromtimestamp(timestamp)
    return timeArray.strftime("%Y-%m-%d %H:%M:%S")

def localtime_to_datetime() -> datetime:
    pass

def len_int(n: int) -> int:
    """
    :param n: 输入数字
    :return: 数字长度
    返回数字长度
    """
    if n > 0:
        digits = int(math.log10(n)) + 1
    elif n == 0:
        digits = 1
    else:
        digits = int(math.log10(-n)) + 2
    return digits

if __name__ == '__main__':
    print(timestamp_to_datetime("1615545398"))