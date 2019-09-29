#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_parserconf.py
@Author: JACK
@Date  : 2019/8/29
@Des   :
"""
import configparser


class ParserConf(object):
    def __init__(self, path):
        self.c = configparser.ConfigParser()
        self.c.read(path)

    def sections(self):
        return self.c.sections()

    def options(self, sec):
        return self.c.options(sec)

    def items(self, sec):
        return self.c.items(sec)

    def get_item(self, sec, opt):
        return self.c.get(sec, opt)

    def get_int_item(self, sec, opt):
        return self.c.getint(sec, opt)

    def conf_2_valuepool(self, valuepool):
        if len(self.sections()):
            for i in self.sections():
                if len(self.options(i)) and i == "INIT":
                    for j in self.options(i):
                        valuepool[j] = self.get_item(i, j)
                else:
                    continue
        return










