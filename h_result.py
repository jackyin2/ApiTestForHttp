#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : result.py
@Author: JACK
@Date  : 2019/8/23
@Des   :
"""

import time, datetime
from jinja2 import Template
from h_init import GENARATE_RESULT, CASE_BOX
from h_log import logO
import os


path = os.path.abspath(__file__).split('\\')
path.pop()
path = '\\'.join(path)
templatepath = os.path.join(path, "template/report_template.html")

class Reportor(object):
    """
    report生成器
    """
    def __init__(self,  report_name=None, type=None, genarate_result=GENARATE_RESULT):
        self.template = templatepath
        self.genarate_result = genarate_result
        if report_name is None:
            self.report_name = self._make_report_name()
        else:
            self.report_name = report_name
        self.type = type
        self.r = None

    def _make_report_name(self):
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        # reportpath1 = os.path.abspath(os.path.join(os.getcwd(), '..\\report'))
        report_name = "Api_test_report" + now + ".html"
        return report_name

    def _read_template(self):
        logO.info("1： read_report")
        with open(self.template, 'r', encoding='UTF-8') as f:
            t = f.read()
            tp = Template(t)
            self.r = tp.render(success=self._count_success(),
                               all_message=self._get_all_message(),
                               all=self._count_all(),
                               fail=self._count_failure(),
                               fail_messages=self._get_failure_message(),
                               avgtime=self._avg_time(),
                               maxtime=self._max_time(),
                               mintime=self._min_time(),
                               files_count=self._count_all_files(),
                               error_count=self._count_error_files())
        return self.r

    def _new_report(self):
        logO.info("2： report-success")
        with open(path + "./report/"+self.report_name, 'w', encoding="utf8") as f:
            f.write(self.r)

    def _is_report(self):
        pass

    def _report(self):
        if self.report_name.endswith(self.type):
            self._read_template()
            self._new_report()
        else:
            print("当前生成的报告非指定格式{}".format(self.type))

    # 统计所有case总和
    def _count_all(self):
        return len(self.genarate_result)

    # 统计成功的case总和
    def _count_success(self):
        return len([s for s in self.genarate_result if s.caseresult == True])

    # 统计失败的case总和
    def _count_failure(self):
        return len([f for f in self.genarate_result if f.caseresult is False])

    # 展示所有的case记录
    def _get_all_message(self):
        return [f for f in self.genarate_result]

    # 获取失败的case记录
    def _get_failure_message(self):
        return [f for f in self.genarate_result if f.caseresult == False]

    # 统计平均响应时间
    def _avg_time(self):
        try:
            avg = sum([t.runtime for t in self.genarate_result if t.caseresult == True])/self._count_success()
        except ZeroDivisionError as e:
            return 0
        return avg

    # 统计最大响应时间
    def _max_time(self):
        try:
            m = max([t.runtime for t in self.genarate_result if t.caseresult == True])
        except ValueError as e:
            return 0
        return m

    # 统计最小响应时间
    def _min_time(self):
        try:
            m = min([t.runtime for t in self.genarate_result if t.caseresult == True])
        except ValueError:
            return 0
        return m

    def _count_all_files(self):
        return len(set([s.filename for s in self.genarate_result]))

    def _count_error_files(self):
        return len([s.filename for s in self.genarate_result if s.casemessage == "JsonFileReadFail"])

    def _error_files(self):
        return [s for s in self.genarate_result if s.casemessage == "JsonFileReadFail"]


class HtmlReportor(Reportor):

    def __init__(self, report_name, type="html"):
        super(HtmlReportor,self).__init__(report_name, type)

    def report(self):
        logO.info("*********report*******")
        self._report()


class TextReportor(Reportor):
    def __init__(self, report_name):
        super(TextReportor,self).__init__(report_name)

    def report(self):
        self._report()














