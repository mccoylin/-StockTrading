#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import tushare as ts
import numpy as np
import time
from datetime import date, datetime
from chinese_calendar import is_workday,is_holiday
# pro = ts.pro_api('17649607a4e92be1fe38fb52b2ff2e044ac6301f665e98b278ab14a7')

# data = pro.stock_basic(exchange='SSE', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')


# getworkday() 函數的功能是檢查當天是否為工作日。以下是該函數的詳細步驟：
def getworkday():
    # chinese_calendar 模組可以直接傳入 datatime.date 不用轉換
    # strt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # strt = strt.split("-")
    # y = int(strt[0])
    # m = int(strt[1])
    # d = int(strt[2])
    # april_last = date(y , m , d)
    
    strt = datetime.now().date()

    april_last =  strt

    print(april_last)
    print(is_workday(april_last))
    print("fuckshit",is_holiday(april_last))
    print("dick",not is_holiday(april_last))
    print("elecshit",is_workday(april_last) and (not is_holiday(april_last)))
    return is_workday(april_last) and (not is_holiday(april_last))


# getRtQuotes(t) 函數的功能是根據當天是否為工作日來獲取實時股票數據。
# 如果是工作日，則從 tushare 獲取當天的股票交易數據，並將其轉換為兩個列表返回；
# 如果不是工作日，則返回預設值。
# t : 股票代號
def getRtQuotes(t):

    f = getworkday()

    df = "0"
    resx="0"
    res = "0"
    resy="0"

    print(t)

    if not (f):
        return 0,resx,resy

    print(f)

    strt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print(strt)

    df = ts.get_today_ticks(t)
    print(df)
    res = np.array(df)
    resx = res[:, [0]]  # Extract the first column
    resy = res[:, [1]]  # Extract the second column
    resx = resx.reshape(-1)  # Flatten the array
    resy = resy.reshape(-1)  # Flatten the array
    resx = resx.tolist()  # Convert to list
    resy = resy.tolist()  # Convert to list

    return 1,resx,resy


if __name__ == '__main__':
    getRtQuotes('000001')
