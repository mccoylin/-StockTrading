#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# 移除 mysql 裡的 stocktrading.user_table 欄位 'photo_url' 前的 '..' 兩個字元
# 更新 stocktrading.user_table 欄位 'phone_number'
#
# 使用 mysql.connector.connect() 連線到 mysql
# 使用 RE 處理字串，不會造成多跑幾回就刪掉必要的字
# 使用 pandas 轉成 DataFrame, 容易使用欄位名稱


import mysql.connector
import pandas as pd
import re
from mysql_connect import get_mysql_connection


# 查詢出 user_table 裡的資料, 取出 phone_number, photo_url 欄位就夠。
sql_user_table = "select phone_number, photo_url from user_table;"

# 更新 user_table 裡的 photo_url，phone_number 是 key
sql_update = "update user_table set photo_url=%s where phone_number=%s;"

conn = get_mysql_connection()

with conn:
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(sql_user_table)
        data = cursor.fetchall()

        # 用 pandas 轉成 DataFrame
        data = pd.DataFrame(data)

        values_list = []
        # 取出 photo_url 欄位的資料
        for index, row in data.iterrows():
            # 用 RE 移除 photo_url 前的 '..'
            photo_url = re.sub(r'^\.\.', '', row['photo_url'])
            value = (photo_url, row['phone_number'])
            # 加回 list
            values_list.append(value)

        # 更新 mysql
        cursor.executemany(sql_update, values_list)         # 一次傳 list, 比較省時間
        conn.commit()

        print(f'處理 tranding.user_table "photo_url" 欄位，資料 {len(data)} 筆')
        # print(values_list)
