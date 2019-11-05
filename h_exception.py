#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_exceptions.py
@Author: JACK
@Date  : 2019/9/6
@Des   : 自定义一些异常类
"""


class MyExcepiton(Exception):
    def __str__(self):
        return ("异常：{}".format(
            self.__class__.__name__))

class JsonError(MyExcepiton):
    """
    所有Json相关的错误父类
    """
    def __init__(self, j=None):
        self.j = j

class ParseJsonError(JsonError):
    def __str__(self):
        return ("exception：{}, message：parse json {} error ".format(
            self.__class__.__name__, self.j))

class NotJsonError(JsonError):
    def __str__(self):
        return ("exception：{}, message：{} is not json ".format(
            self.__class__.__name__, self.j))

class LoadJsonFileError(JsonError):
    def __str__(self):
        return ("exception：{}, message：from file:{} load api error".format(
            self.__class__.__name__, self.j))

class NotEqualError(MyExcepiton):
    def __init__(self, a=None, b=None, m=None):
        self.a = a
        self.b = b
        self.m = m

    def __str__(self):
        return ("exception：{}, method:{},  message:{}  ！=  {}".format(
            self.__class__.__name__, self.m, self.a, self.b))

class NotContainError(MyExcepiton):
    def __init__(self, a=None, b=None, m=None):
        self.a = a
        self.b = b
        self.m = m

    def __str__(self):
        return ("exception：{}, method:{},  message:{} not found {}".format(
            self.__class__.__name__, self.m, self.a, self.b))

class NotFoundParams(MyExcepiton):
    def __init__(self, p=None):
        self.p = p

    def __str__(self):
        return ("exception：{}, message:not found params {}".format(
            self.__class__.__name__, self.p))

class ParamsError(MyExcepiton):
    def __init__(self, p=None):
        self.p = p

    def __str__(self):
        return ("{}".format(self.p))

class EvalError(MyExcepiton):
    def __init__(self, p=None, m=None):
        self.p = p
        self.m = m

    def __str__(self):
        return ("exception:{}, method:{}, message:eval {} error".format(
            self.__class__.__name__, self.m,  self.p))

class RequestError(MyExcepiton):
    def __init__(self, a=None):
        self.a = a

    def __str__(self):
        return ("exception：{}, message： {}".format(
            self.__class__.__name__, self.a))

class TimeOutError(RequestError):
    def __str__(self):
        return ("exception：{}, request timeout： {}".format(
            self.__class__.__name__, self.a))

class MySqlError(Exception):
    pass