#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : hcase.py
@Author: JACK
@Date  : 2019/9/27
@Des   :
"""


class TCase(object):
    def __init__(self):
        self._filename = ""
        self._casename = ""
        self._casetype = ""
        self._provider = ""
        self._date = ""
        self._casestep = []
        self._caseresult = False
        self._casemessage = ""
        self._runtime = 0

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, v):
        self._filename = v

    @property
    def casename(self):
        return self._casename

    @casename.setter
    def casename(self, v):
        self._casename = v

    @property
    def casetype(self):
        return self._casetype

    @casetype.setter
    def casetype(self, v):
        self._casetype = v

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, v):
        self._provider = v

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, v):
        self._date = v

    @property
    def casestep(self):
        return self._casestep

    @casestep.setter
    def casestep(self, v):
        self._casestep.append(v)

    @property
    def caseresult(self):
        return self._caseresult

    @caseresult.setter
    def caseresult(self, v):
        self._caseresult = v

    @property
    def casemessage(self):
        return self._casemessage

    @casemessage.setter
    def casemessage(self, v):
        self._casemessage = v

    @property
    def runtime(self):
        return self._runtime

    @runtime.setter
    def runtime(self, v):
        self._runtime = v


class Api(object):
    def __init__(self, name=None, setup=None, request=None, validate=None, collect=None, teardown=None):
        self._name = name
        self._setup = setup
        self._request = request
        self._validate = validate
        self._collect = collect
        self._teardown = teardown
        self._result = False
        self._time = 0
        self._response = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def setup(self):
        return self._setup

    @setup.setter
    def setup(self, v):
        self._setup = v

    @property
    def teardown(self):
        return self._teardown

    @teardown.setter
    def teardown(self, v):
        self._teardown = v

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, v):
        self._request = v

    @property
    def validate(self):
        return self._validate

    @validate.setter
    def validate(self, v):
        self._validate = v

    @property
    def collect(self):
        return self._collect

    @collect.setter
    def collect(self, v):
        self._collect = v

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, v):
        self._time = v

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, v):
        self._result = v

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, v):
        self._response = v
