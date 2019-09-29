#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_assert.py
@Author: JACK
@Date  : 2019/8/28
@Des   : 主要是用于扩展检查几个校验方式，code， str， json， headers
"""
import json
from h_utils import reg_str
from h_exception import ParseJsonError, NotEqualError, NotJsonError, NotContainError


def assertEqCode(r, vali):
    if vali.get("assertEqCode") is None or r.status_code == vali["assertEqCode"]:
        return True
    raise NotEqualError(r.status_code, vali["assertEqCode"], "assertCode")


def assertEqHeaders(r, vali):
    """
    判断headers是否一样
    :param r: 
    :param vali: 
    :return: 
    """
    if vali.get("assertEqHeaders") is None:
        pass
    else:
        for k, v in vali["assertEqHeaders"].items():
            if vali["assertEqHeaders"][k] == r.headers[k]:
                continue
            else:
                raise NotEqualError(vali["assertEqHeaders"][k], r.headers[k], "assertHeaders")
    return True


def assertEqStr(r, vali):
    """
    断言关键字字符串是否存在
    :param r: 
    :param vali: 
    :return: 
    """
    if vali.get("assertEqStr") is None:
        pass
    else:
        l = vali["assertEqStr"]
        for s in l:
            # 正则search
            if reg_str(s, r.text):
                continue
            else:
                raise NotContainError(r.text, s, "assertStr")
    return True


def assertEqJson(r, vali):
    if vali.get("assertEqJson") is None:
        return True
    vl = vali["assertEqJson"]
    if not isinstance(vl, dict):
        raise NotJsonError(vl)
    try:
        jt = json.loads(r.text)
    except:
        raise NotJsonError(r.text)

    for k, v in vl.items():
        if jt.get(k) is None:
            print("response找不到validator中的的json字段---", end="")
        if vl[k] != jt[k]:
            raise NotEqualError(vl[k], jt[k], "assertJson")
        else:
            continue
    return True

