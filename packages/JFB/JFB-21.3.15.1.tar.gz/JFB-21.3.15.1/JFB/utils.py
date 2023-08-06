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
                    2021-03-15：功能更新
-------------------------------------------------
"""
__author__ = 'jiangfb'

import datetime
import math
from datetime import datetime as dt
from datetime import timedelta


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

def timestamp_to_datetime(timestamp) -> str:
    """
    :param timestamp: 字符串或整形型时间戳(10/13位均可)
    :return: localtime类型
    时间戳转格式化字符串类型
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

def localtime_to_datetime(localtime: str) -> datetime:
    """
    :param localtime: 本地时间格式字符串
    :return: datetime格式
    时间格式字符串转datetime类型
    """
    return datetime.datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')

def get_delta_datetime(days: float) -> datetime:
    """
    :param days: 间隔的时间天数
    :return: days天前的日期
    获取指定时间前的日期
    """
    if days == -1:
        return dt.strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    now = dt.now()
    delta = timedelta(days=days)
    n_days_forward = now - delta
    return n_days_forward

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