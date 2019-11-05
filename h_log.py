#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Author  : Jack
# @FileName: h_log.py
# @Time    : 2019/11/5 10:40

"""
   关于控制log文件输出
"""


import logging
# logging.basicConfig(level=logging.DEBUG,
#                     format="%(asctime)s %(name)s %(levelname)s %(message)s",
#                     datefmt = '%Y-%m-%d  %H:%M:%S %a',    #注意月份和天数不要搞乱了，这里的格式化符与time模块相同
#                     filename='./log.txt'
#                     )
#
#
# logging.debug("debug")
# logging.info("info")
# logging.error("error")
# logging.warning("warm")

def log():
    # 创建logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # 设置logger日志等级

    # 判断是否有handlers
    if not logger.handlers:
        filehandler = logging.FileHandler("./log/log.txt", encoding='utf-8')
        cmdhandler = logging.StreamHandler()

        # 设置输出日志格式
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] %(name)s %(filename)s %(message)s",
            datefmt="%Y/%m/%d %X"
        )

        # 为handler指定输出格式
        filehandler.setFormatter(formatter)
        cmdhandler.setFormatter(formatter)

        # 为logger添加日志处理器
        logger.addHandler(filehandler)
        logger.addHandler(cmdhandler)

    return logger  # 直接返回logger


logO = log()





