#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-8

@author: Xu
"""
import os
import configparser


# 获取config配置文件
def get_config(section, key):
    config = configparser.ConfigParser()
    # os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录也可以用下方os.path
    path = os.path.join(os.path.dirname(__file__), 'settings.conf')
    config.read(path)
    return config.get(section, key)


logger_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
