#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : h_result.py
@Author: JACK
@Date  : 2019/9/27
@Des   :
"""
import os
import time
import requests
from addict import Dict
from functools import wraps
from h_loader import load_cases_from_file, load_cases_from_dir
from h_utils import *
from h_init import CASE_BOX, GENARATE_RESULT, VALUE_POOLS
from h_parser import ParserConf
from h_exception import *
from h_assert import *
from h_log import logO


# 装饰器
def take_up_time(func):
    @wraps(func)
    def warpper(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        end = time.time()
        t = end-start
        return f, round(t, 4)
    return warpper

# api请求重试
def requests_retry(times=3):
    def decorater(func):
        def inner(*args, **kwargs):
            case, var = args
            t = times
            i = 0
            while t:
                try:
                    f = func(*args, **kwargs)
                except RequestError as e :
                    logO.error("num {} retry  requests : {}".format(i+1, parameters(case.request["url"], var, VALUE_POOLS)))
                    t -= 1
                    i += 1
                    f = None
                    if i == times:
                        raise RequestError(e)
                else:
                    t = 0
            return f
        return inner
    return decorater



def init_g_variable(test_dir):
    # 初始化加载全局配置
    for root, dirs, filenames in os.walk(test_dir):
        if filenames == []:
            continue
        else:
            for name in filenames:
                # 区分测试用例文件和初始化参数文件
                if name.startswith("Init") and name.endswith(".ini"):
                    conf_path = root + "\\" + name
                    p = ParserConf(conf_path)
                    p.conf_2_valuepool(VALUE_POOLS)
                break
        break


def cases_from_dir_or_file(path):
    if is_dir(path):
        load_cases_from_dir(path)
    elif is_file(path):
        load_cases_from_file(path)


count = 0
def runner(casebox):
    """
    执行case
    :param casebox: 
    :return: 
    """
    for tcase in casebox:
        global count
        count += 1
        # 0 判断文件读取失败的记录
        if tcase.casemessage == "JsonFileReadFail":
            logO.info("*****当前执行第 {} 个 case：{}, message: {}********".format(count, tcase.filename, tcase.casemessage))

            # GENARATE_RESULT.append(tcase)
            continue

        # 1 正常读取文件，执行case
        logO.info("*****当前执行第 {} 个 file:{}  case：{}********".format(count, tcase.filename, tcase.casename))
        apis = tcase.casestep
        for case in apis:
            if tcase.casetype == "api":
                logO.info("###### api: {} ######".format(case.name))
            else:
                logO.info("###### step: {} ######".format(case.name))

            try:
                # 0 请求前参数准备
                var = setup(case)

                # 1 请求接口
                re, runtime = runapi(case, var)
                if re is not None:
                    case.response = re.text

                # 2 校验接口
                istrue = validate(case, re)
                if istrue:
                    case.result = True
                    case.time = runtime
                    tcase.caseresult = True
                    tcase.runtime = tcase.runtime + case.time

                # 3 提取参数
                collect(case, re, var)

                # 4 清理var
                teardown(var)
            except Exception as e:
                logO.debug("error : {}".format(e))
                case.response = e
                tcase.casemessage = e
                break

            else:
                case.collect = True



@take_up_time
@requests_retry(times=3)
def runapi(case, var):
    """
    执行api，返回请求内容
    :param file: 
    :param case: 
    :param v_setup: 
    :return: 
    """
    _request = case.request
    try:
        url = parameters(_request["url"], var, VALUE_POOLS)
        method = parameters(_request["method"], var, VALUE_POOLS).lower()
        headers = parameters(_request["headers"], var, VALUE_POOLS)
        data = parameters(_request["data"], var, VALUE_POOLS)
    #  此处判断是否存在文件需要处理
        if _request.get("files"):
            filedicts = parameters(_request["files"], var, VALUE_POOLS)
            _files = {}
            for filekey, filevalue in filedicts.items():
                _files[filekey] = post_files(replace_path(filevalue))
        else:
            _files = None
    except NotFoundParams as e:
        logO.error("2: runapi > error: {}".format(e))
        raise ParamsError(e)

    # 执行请求
    try:
        if method not in ["post", 'patch', "delete", "put"]:
            re = requests.get(url=url, params=data, headers=headers)
        else:
            if headers.get("Content-Type") and headers["Content-Type"] == "application/json":
                re = requests.request(method=method, url=url, json=data, files=_files, headers=headers, timeout=2)
            else:
                re = requests.request(method=method, url=url, data=data, files=_files, headers=headers, timeout=2)
    except Exception as e:
        re = None
        logO.error("2: runapi > error: {}".format(e))
        raise RequestError(e)
    logO.info("2: runapi > ok")
    return re


def validate(case, re):
    """
    校验请求返回结果是否正确
    :param case: 
    :param re: 
    :return: 
    """
    if re is None:
        logO.info("3: validate >  fail")
        return False

    val = case.validate
    count = 0
    if assertEqCode(re, val):
        count += 1
    if assertEqStr(re, val):
        count += 1
    if assertEqHeaders(re, val):
        count += 1
    if assertEqJson(re, val):
        count += 1
    if count >= len(val):
        logO.info("3: validate >  True")
        return True
    if count < len(val):
        logO.info("3: validate >  False")
    return False


def collect(case, re, var):
    """
    提取相关内容，提供给后期接口使用
    :param case: 
    :param re: 
    :param var: 
    :return: 
    """

    coll = case.collect
    try:
        response = json.loads(re.text)
    except Exception as e:
        logO.error("4: collect > 解析{}json格式错误,错误信息{}".format(re, e))
        raise NotJsonError(re.text)
        # return False

    response = Dict(response)
    for k, v in coll.items():
        # 此处判断如果是json，则用链式取值，如果是方法，则用正则来进行匹配获取
        if k == "json":
            for k1, v1 in v.items():
                # 通过eval直接执行获取对应的json值
                try:
                    v1 = eval(v1)
                except Exception:
                    raise EvalError(v1, "Json_collect")
                VALUE_POOLS[k1] = v1
                # VALUEPOOLS.update(k1=v1)
        elif k == "methods":
            for k2, v2 in v.items():
                method = is_method(str(v2))
                # 判断方法中是否还存在入参的参数化
                if method and is_params(method):
                    method = parameters(method, var, VALUE_POOLS)
                try:
                    VALUE_POOLS[k2] = eval(method)
                except Exception:
                    raise EvalError(method, "Method_collect")
        elif k == "values":
            for k3, v3 in v.items():
                VALUE_POOLS[k3] = parameters(v3, var, VALUE_POOLS)
    logO.info("4: collect > ok")


def teardown(var):
    if len(var) > 0:
        clear_value(var)
        logO.info("5: teardown > ok")
    return


def setup(case):
    """
    主要用于接口执行前的相关参数准备
    eg：  
        "a" : 1,
        "b" : "str"
        "m1" : "${__method(a,b)}",
        "m2" : "${__method(a, ${a}, '${b}')}"
    :param case: 
    :return: 
    """

    vals = case.setup
    _vals = {}
    # 1 首先_vals先加载方法中不存在$的方法和正常的值
    try:
        for key, val in vals.items():
            # 判断是否是一个待执行的方法，
            method = is_method(str(val))
            if method:
                if is_params(method):
                    continue
                # 判断当前的方法是否还需要继续参数化，如果需要参数化，则等待后面执行
                _vals[key] = eval(method)
            elif not method:
                if is_params(str(val)):
                    continue
                # 如果不要参数化，判断下是不是路径式字段是则转换
                _vals[key] = replace_path(val)

        # 2 加载非方法内的字符串参数化
        for k1, v1 in vals.items():
            method = is_method(str(v1))
            if not method and is_params(str(v1)):
                v1 = parameters(v1, _vals, VALUE_POOLS)
                _vals[k1] = v1

        # 此处加载方法中带有参数$ 和 字符串中带有$
        for k, v in vals.items():
            method = is_method(str(v))
            if method and is_params(method):
                method = parameters(method, _vals, VALUE_POOLS)
                _vals[k] = eval(method)
    except NotFoundParams as e:
        logO.error("1: setup > error {}".format(e))
        raise ParamsError
    except MySqlError as e:
        logO.error("1: setup > error {}".format(e))
        raise MySqlError

    logO.info("1: setup > ok")
    return _vals





