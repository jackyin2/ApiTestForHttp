#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : tester.py.py
@Author: JACK
@Date  : 2019/9/27
@Des   :
"""
#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : cmd.py.py
@Author: JACK
@Date  : 2019/9/19
@Des   :
"""
import argparse
from h_main import *
from h_utils import check_json, is_path


# 2 命令行执行
parser = argparse.ArgumentParser(description="这是一款测试api的小框架，具有参数化，异常定位等特性")
parser.add_argument("-p", "--path", help="测试内容，可以是文件也可以是路径", type=str, required=True)
parser.add_argument("-cf", "--conf", help="配置文件路径", type=str, default=None)
parser.add_argument("-r", "--report", help="测试报告", type=str)
parser.add_argument("-CK", "--check", help="json文件检查", type=int, default=0)
args = parser.parse_args()
if not is_path(args.path):
    print("is not a true path ,please check! ")
    exit(0)
# elif args.conf is not None:
#     print("is not a true conf path ,please check! ")
#     exit(0)
elif args.check == 1:
    check_json(args.dir)
    exit(0)
main(path=args.path, conf_path=args.conf, report_name=args.report)