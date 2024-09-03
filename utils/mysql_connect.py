#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# 獨立出 mysql 連線的部分，方便其他程式引用。
# 只需要修改一次。 
#
# 叫用方式：
# from mysql_connect import get_mysql_connection

import mysql.connector


# Connect to the database
def get_mysql_connection():
	return mysql.connector.connect(
		host="127.0.0.1",
		port=3306,
		user="trading",
        password = "YOUR_PASSWORD_記得修改",
		db="stocktrading",
		charset="utf8mb4"
	)
