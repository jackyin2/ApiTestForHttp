#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : h_main.py
@Author: JACK
@Date  : 2019/9/27
@Des   :
"""

from h_runer import init_g_variable, runner, cases_from_dir_or_file
from h_init import CASE_BOX
from h_result import HtmlReportor


def main(path=None, conf_path=None, report_name=None):

    # 0 初始化配置文件
    if conf_path is None:
        init_g_variable(path)
    else:
        init_g_variable(conf_path)


    # 1 加载case到CASE_BOX
    cases_from_dir_or_file(path)

    # 2 执行case
    runner(CASE_BOX)

    # 3 生成报告
    if report_name != "N":
        report = HtmlReportor(report_name=report_name)
        report.report()


if __name__ == "__main__":
    main("E:\jackstudy\ApiTestForHttp\data\custemor_V2.0")