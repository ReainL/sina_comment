#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-8

@author: Xu
"""
import psycopg2
import config


def get_conn():
    database = config.get_config("db_param", "database")
    user = config.get_config("db_param", "user")
    password = config.get_config("db_param", "password")
    host = config.get_config("db_param", "host")
    port = config.get_config("db_param", "port")
    try:
        conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    except Exception as e:
        raise Exception("连接数据库出错：%s", repr(e))
    return conn


def execute_select(conn, sql, params=None):
    with conn.cursor() as cur:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        return cur.fetchall()


def execute_sql(conn, sql, params=None):
    with conn.cursor() as cur:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)


def get_engine():
    database = config.get_config("db_param", "database")
    user = config.get_config("db_param", "user")
    password = config.get_config("db_param", "password")
    host = config.get_config("db_param", "host")
    try:
        code_engine = 'postgres://' + user + ':' + password + '@' + host + '/' + database
    except Exception as e:
        raise Exception("连接数据库出错：%s", repr(e))
    return code_engine
