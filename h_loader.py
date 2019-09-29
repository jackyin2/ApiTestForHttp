#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : h_loader.py
@Author: JACK
@Date  : 2019/9/27
@Des   :
"""
import json , os
from h_case import Api, TCase
from h_init import CASE_BOX


def find_all_file(path):
    """
    查找所有的需要执行测试case文件
    :param path: 
    :return: 
    """
    files = []
    all_files = os.walk(path)
    for root, dirs, filenames in all_files:
        if filenames == []:
            continue
        else:
            for name in filenames:
                # 区分测试用例文件和初始化参数文件
                if name.startswith("test_") and \
                        (name.endswith(".json") or name.endswith(".yaml")):
                    files.append(os.path.join(root, name))
    return files


def load_cases_from_dir(path):
    files = find_all_file(path)
    for file in files:
        add_cases(file)


def load_cases_from_file(file_path):
    """
    从指定文件中加载case
    :param file_path: 
    :return: 
    """
    add_cases(file_path)


def add_cases(path):
    """
    加载所有的json对象到cases列表中
    :param path: 
    :return: 
    """
    f_name = path.split("\\")[-1]
    with open(path, "r", encoding="utf-8") as _f:
        try:
            # f_dict = json.load(f).decode(encoding='gbk').encode(encoding='utf-8')
            f_dict = json.load(_f)
        except Exception as e:
            tc = TCase()
            tc.filename = f_name
            tc.casemessage = "JsonFileReadFail"
            CASE_BOX.append(tc)
        else:
            if f_dict["type"].lower() == "api" and f_dict.get("test"):
                for test in f_dict["test"]:
                    tc = TCase()
                    tc.filename = f_name
                    tc.casename = test["name"]
                    tc.casetype = f_dict["type"]
                    tc.provider = f_dict["author"]
                    tc.date = f_dict["date"]
                    api = Api(name=test["name"],
                              setup=test["setup"],
                              request=test["requestor"],
                              collect=test["collector"],
                              teardown=test["teardown"],
                              validate=test["validator"])
                    tc.casestep = api
                    CASE_BOX.append(tc)
            elif f_dict.get("type").lower() == "scene" and f_dict.get("test"):
                tc = TCase()
                tc.filename = f_name
                tc.casename = f_dict["name"]
                tc.casetype = f_dict["type"]
                tc.provider = f_dict["author"]
                tc.date = f_dict["date"]
                for test in f_dict["test"]:
                    api = Api(name=test["name"],
                              setup=test["setup"],
                              request=test["requestor"],
                              collect=test["collector"],
                              teardown=test["teardown"],
                              validate=test["validator"])
                    tc.casestep = api
                CASE_BOX.append(tc)








