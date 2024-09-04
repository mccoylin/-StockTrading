#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import pymysql
import tushare as ts
import numpy as np
import time
# 同一個資料夾下的 getHistoryData.py
# from utils import getHistoryData
from getHistoryData import getHistoryData
from mysql_connect import get_pymysql_connection


# 会连接到本地的 stocktrading 数据库，并创建一个名为 t 的表，用于存储股票的历史数据。表的字段包括交易日期、开盘价、最高价、最低价和收盘价。
def createStockTable(t):  # 建表 eg:表名为000001.SZ，字段是日期，开盘，最高，最低,收盘
    conn = get_pymysql_connection()
    cursor = conn.cursor()
    sql = """CREATE TABLE `%s`(
                 TRADING_DAY VARCHAR(64) DEFAULT NULL,
                 OPEN_PRICE FLOAT DEFAULT NULL,
                 HIGHEST FLOAT DEFAULT NULL,
                 LOWEST FLOAT DEFAULT NULL,
                 CLOSE_PRICE FLOAT DEFAULT NULL)
                """
    cursor.execute(sql, [t])


# 在 stocktrading 數據庫中創建一個用於存儲每天實時數據的表。
# 創建一個用於存儲每天實時數據的表，表名為 dailyTicks_<t>。
def createEvedayTable(t):  # 每天实时数据

    # 使用 %s 會存傳入字串時，會有單引號，所以改用 f-string
    #sql = """CREATE TABLE %s(
    #             DAILY_TICKS VARCHAR(64) DEFAULT NULL,
    #             REAL_TIME_QUOTES FLOAT DEFAULT NULL
    #             )
    #            """
    # cursor.execute(sql, ["dailyTicks_" + t])
    
    ## 多行的字串會有換行符號，還需處理
    #sql = f"""CREATE TABLE daily_{t} ( DAILY_TICKS VARCHAR(64) DEFAULT NULL, REAL_TIME_QUOTES FLOAT DEFAULT NULL) """

    sql = f"""CREATE TABLE `{t}`(
                 DAILY_TICKS VARCHAR(64) DEFAULT NULL COMMENT '實時報價',
                 REAL_TIME_QUOTES FLOAT DEFAULT NULL COMMENT '報價時間'
                 )  
                """

    ## 多行的字串會有換行符號，還需處理
    #sql1 = sql.replace('\n', '')    

    result = search_table_exist(t)
    if result:
        print(f'{t} 已存在！')
        return

    conn = get_pymysql_connection()
    cursor = conn.cursor()

    cursor.execute(sql)

    cursor.close()
    conn.close()


# 將歷史股票數據插入到 stocktrading 數據庫中的指定表中。
def InsertOldDay(t):
    res = getHistoryData.getHistoryData(t)
    print(res)
    conn = get_pymysql_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO `%s`(TRADING_DAY,OPEN_PRICE,HIGHEST,LOWEST,CLOSE_PRICE) VALUES(%s, %s, %s, %s,%s)"
    t = t.split(".")

    for i in res:
        i.insert(0, t[0] + "_" + t[1])
        # print(i)
        cursor.execute(sql, i)
        conn.commit()
    cursor.close()
    conn.close()


# 將當天的股票交易數據插入到 stocktrading 數據庫中的指定表中。
def insertTodayTickData(t):
    t = t.split(".")
    res = ts.get_today_ticks(t[0])
    conn = get_pymysql_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO `%s`(TRADING_DAY,OPEN_PRICE,HIGHEST,LOWEST,CLOSE_PRICE) VALUES(%s, %s, %s, %s,%s)"

    for i in res:
        i.insert(0, t[0] + "_" + t[1])
        # print(i)
        cursor.execute(sql, i)
        conn.commit()
    cursor.close()
    conn.close()


# 从数据库中获取股票信息，并根据股票类型生成特定格式的股票代码，然后调用 InsertOldDay 函数处理这些股票代码。
def getTscode():
    conn = get_pymysql_connection()
    cursor = conn.cursor()
    sql = "select stock_id,stock_type  from stock_info"
    cursor.execute(sql)
    stoinfo = cursor.fetchall()
    for i in range(959,len(stoinfo)):
        if(stoinfo[i][1] == "上证"):
            tmp=stoinfo[i][0]+"_"+"SH"
            # tmp = stoinfo[i][0] + "." + "SH"

        else:
            tmp = stoinfo[i][0] + "_" + "SZ"
            # tmp = stoinfo[i][0] + "." + "SZ"
        # createStockTable(tmp)
        # createEvedayTable(tmp)
        print(tmp)
        InsertOldDay(tmp)
        # time.sleep(1)
    cursor.close()
    conn.close()


# 删除指定的 table
def delete_Table_if_exist(table_name):

    conn = get_pymysql_connection()
    cursor = conn.cursor()

    # table 存在會刪除 
    sql_drop = f"DROP TABLE IF EXISTS `{table_name}`"

    cursor.execute(sql_drop)

    cursor.close()
    conn.close()


# 尋找 table_name 是否存在
# 原來找到的語法可能因為模組實作的問題而無法使用，
# 所以 w3cschool 才會提供用 show tables 來找
def search_table_exist(table_name) -> bool:
    conn = get_pymysql_connection()
    cursor = conn.cursor()
    sql = "SHOW TABLES;"
    # mysql workbench 可以執行的語法，但 pymysql 會有問題
    # sql = f"""SELECT EXISTS ( SELECT * FROM information_schema.tables WHERE table_schema = 'stocktrading' AND table_name = `{table_name}` );"""

    cursor.execute(sql)
    tables = cursor.fetchall()

    cursor.close()
    conn.close()

    # 在 tuple 找出 table_name
    find = [table for table in tables if table[0] == table_name]       # 沒找到是空的
    if len(find) == 0:
        print(f"{table_name} 不存在！")
        return False
    
    print(f"找到 {table_name}")
    return True



# getTscode()
# InsertOldDay("000001.SZ")


if __name__ == '__main__':
    createEvedayTable('a2d3f4f5')
    delete_Table_if_exist('a2d3f4f5')


