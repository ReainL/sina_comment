#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-9

@author: Xu
"""
import jieba
import numpy as np
import matplotlib.pyplot as plt
import logging.config

from config import logger_path
from scipy.misc import imread
from snownlp import SnowNLP
from wordcloud import WordCloud, ImageColorGenerator
from collections import Counter
from common.pgutils import get_conn, execute_select


logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


def read_comment(conn):
    logger.info('读取数据库中数据...read_comment')
    sina_li = []
    comment_li = []
    user_li = []
    sql_select = "SELECT * FROM sina_comment"
    params = '1000'
    result = execute_select(conn, sql_select)
    logger.debug(result)
    for res in result:
        logger.debug(res)
        if res not in sina_li:
            sina_li.append([res[0],
                            res[1],
                            res[2],
                            res[3],
                            res[4]])
            user_name = res[1]
            user_li.append(user_name)
            comment = res[3]
            if comment:
                comment_li.append(comment)
    return sina_li, comment_li, user_li


def word_cloud(comment):
    logger.info('制作词云图...word_cloud')
    comment_text = ''
    back_coloring = imread("static/heart.jpg")
    cloud = WordCloud(font_path='static/simhei.ttf',  # 为了保证中文正常显示,需要加上字体
                      background_color="white",  # 背景颜色
                      max_words=2000,  # 词云显示的最大词数
                      mask=back_coloring,  # 设置背景图片
                      max_font_size=100,  # 字体最大值
                      random_state=42,
                      width=1000, height=860, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                      )
    for li in comment:
        comment_text += ' '.join(jieba.cut(li, cut_all=False))
    wc = cloud.generate(comment_text)
    image_colors = ImageColorGenerator(back_coloring)
    plt.figure("wordc")
    plt.imshow(wc.recolor(color_func=image_colors))
    wc.to_file('微博评论词云图.png')


def snownlp(comment):
    logger.info('自然语言处理NLP...snow_analysis')
    sentimentslist = []
    for li in comment:
        s = SnowNLP(li)
        logger.debug(li, s.sentiments)
        sentimentslist.append(s.sentiments)
    fig1 = plt.figure("sentiment")
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
    plt.show()


def follows(comment):
    logger.info('列出评论数')
    userdict = Counter(comment)
    logger.info(userdict.most_common(20))


if __name__ == '__main__':
    conn = None
    try:
        conn = get_conn()
        with conn:
            sina_list, comment_list, user_list = read_comment(conn)
            word_cloud(comment_list)
            snownlp(comment_list)
            follows(comment_list)
    finally:
        if conn:
            conn.close()
