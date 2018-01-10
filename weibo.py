#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-8

@author: Xu
"""
import re
import time
import sys
import random
import requests
import logging.config

from config import logger_path
from common.collect_ip import get_ip, ua_list
from common.pgutils import get_conn, execute_sql

logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


sql = """
        INSERT INTO public.sina_comment(comment_id, user_name, created_at, comment, like_counts) 
                            VALUES(%s, %s, %s, %s, %s)
    """


def sina(conn, ips):
    logger.debug('新浪微博评论采集...sina')
    ip = random.choice(ips)
    # 指定IP
    uid = '4193705642468999'
    url = 'https://m.weibo.cn/single/rcList?format=cards&id=' + uid + '&type=comment&hot=0&page={}'
    i = 200
    comment_num = 1  # 第几条评论
    try:
        for i in range(i+1, 67000):
            ip = random.choice(ips)
            proxies = {
                'http': ip
            }
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Cookie": "你的cookie",
                "Host": "m.weibo.cn",
                "Referer": "https://m.weibo.cn/status/" + uid,
                "User-Agent": random.choice(ua_list),
                "X-Requested-With": "XMLHttpRequest",
            }
            logger.debug(proxies)
            try:
                logger.debug(url.format(i))
                res = requests.get(url=url.format(i), headers=headers, proxies=proxies)
                r = res.json()
                content = r[0]['card_group']
                if res.status_code == 200:
                    logger.debug('抓取第%s页评论' % i)
                    for j in range(0, len(content)):
                        logger.debug('第%s条评论' % comment_num)
                        hot_data = content[j]
                        comment_id = hot_data['user']['id']  # 用户id
                        user_name = hot_data['user']['screen_name']  # 用户名
                        created_at = hot_data['created_at']  # 评论时间
                        # 评论内容
                        comment = re.sub('<.*?>|回复<.*?>:|[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]', '',
                                         hot_data['text'])
                        like_counts = hot_data['like_counts']  # 点赞数
                        sql_params = [comment_id, user_name, created_at, comment, like_counts]
                        logger.debug(sql_params)
                        execute_sql(conn, sql, sql_params)
                        comment_num += 1
                    time.sleep(random.randint(2, 5))
            except requests.exceptions.ConnectionError:
                logger.debug('ConnectionError')
                if not ips:
                    logger.debug('ip 已失效')
                    sys.exit()
                # 删除不可用的代理IP
                if ip in ips:
                    ips.remove(ip)
    except Exception as e:
        logger.error(e)


def main():
    conn = None
    try:
        conn = get_conn()
        with conn:
            ips = []
            for i in range(6000):
                # 每隔1000次重新获取一次最新的代理IP，每次可获取最新的100个代理IP
                if i % 1000 == 0:
                    ips.extend(get_ip())
            sina(conn, ips)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()




