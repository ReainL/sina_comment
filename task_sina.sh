#!/usr/bin/env bash

SINA_HOME=$(cd `dirname $0`; pwd)

python3 ${SINA_HOME}/weibo.py
python3 ${SINA_HOME}/comment_nlp.py