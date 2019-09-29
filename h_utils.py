#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_utils.py
@Author: JACK
@Date  : 2019/8/23
@Des   :
"""
import re
import json
import base64
import pymysql
import os
import random
from h_exception import NotFoundParams
from h_parser  import ParserConf


def strclass(cls):
    return "%s.%s" % (cls.__module__, cls.__qualname__)


def reg_str(r, st):
    if re.search(r, st):
        return True
    return False


def check_json(path):
    files = []
    errorfiles = []
    all_files = os.walk(path)
    for root, dirs, filenames in all_files:
        if filenames == []:
            continue
        else:
            for name in filenames:
                # 区分测试用例文件和初始化参数文件
                if name.startswith("test_") and \
                        (name.endswith(".json") or name.endswith(".yaml")):
                    file_path = os.path.join(root, name)
                    files.append(file_path)
                    try:
                        f_name = file_path.split("\\")[-1]
                        with open(file_path, "r", encoding="utf-8") as _f:
                            json.load(_f)
                    except Exception as e:
                        errorfiles.append(f_name)
                    # if name.startswith("global_") and name.endswith(".py"):
                    #     pass
    print("当前文件json文件个数：{}, 错误文件个数：{} 为：{}".format(len(files), len(errorfiles), errorfiles))
    # return (len(files),  errorfile)


def is_path(path):
    if os.path.isfile(str(path)) or os.path.isdir(str(path)):
        return True
    return False


def is_file(path):
    if os.path.isfile(str(path)) or path is None:
        return True
    return False


def is_dir(path):
    if os.path.isdir(str(path)):
        return True
    return False


def replace_path(path):
    if is_path(path):
        path = path.replace("\\", "/")
    return path


def is_method(str):
    method = re.search("\$\{\_\_(.+)\}", str)
    if method is None:
        return False
    return method.group(1)


# 是否存在参数化必要
def is_params(obj):
    params = get_params_list_re(obj)
    if len(params) > 0:
        return True
    return False


# 获取需要参数化的个数
def get_params_num(obj):
    if isinstance(obj, str):
        return len(re.findall("\$\{", obj))
    if isinstance(obj, dict):
        str = json.dumps(obj)
        return len(re.findall("\$\{", str))


def get_params_list_sp(obj):
    l = []
    if isinstance(obj, str):
        pass
    elif isinstance(obj, dict):
        obj = json.dumps(obj)
    obj_split = obj.split("$")
    for _v in obj_split:
        if "{" not in _v:
            obj_split.remove(_v)
    for _v_ in obj_split:
        val = re.match("^\{(.*)\}", _v_).group(1)
        l.append(val)
    return l


# re版本获取列表
def get_params_list_re(obj):
    if isinstance(obj, str):
        pass
    elif isinstance(obj, dict):
        obj = json.dumps(obj)
    pattern = '\$\{(.+?)\}'
    l = re.findall(pattern, obj)
    return l


# 当前方法主要用于参数化结果的转化为执行值
def parameters(obj, var, valuepools):
    # 判断如果传值是str对象，那么替换时候不需要eval，直接replace替换
    if isinstance(obj, str):
        paramlist = set(get_params_list_re(obj))
        for i in paramlist:
            r_str = "${" + str(i) + "}"
            if valuepools.get(i) is not None:
                obj = obj.replace(r_str, str(valuepools[i]))
            elif var.get(i) is not None:
                # 此处重点判断是否需要保留原样式
                if type(var[i]) in [int, float, dict, tuple, list]:
                    if len(str(i)) == len(obj) - 3:
                        obj = eval(obj.replace(r_str, str(var[i])))
                    else:
                        obj = obj.replace(r_str, str(var[i]))
                        if obj[0] in ["-", "~"]:
                            obj = obj[1:len(obj)]
                else:
                    obj = obj.replace(r_str, str(var[i]))

                # obj = obj.replace(r_str, str(var[i]))
            elif var.get(i) is not None and valuepools.get(i) is not None:
                obj = obj.replace(r_str, str(var[i]))
            else:
                print("var|valuePool中不存在需要的参数{}".format(i))
                raise NotFoundParams(i)
    elif isinstance(obj, list):
        l = 0
        for o in obj:
            o = parameters(o, var, valuepools)
            obj[l] = o
            l += 1
    elif isinstance(obj, dict):
        for k, v in obj.items():
            v = parameters(v, var, valuepools)
            obj[k] = v
    return obj


def parameters_bak(obj, var, valuepools):
    paramlist = set(get_params_list_re(obj))
    if isinstance(obj, str):
        pass
    elif isinstance(obj, dict):
        obj = json.dumps(obj)
    for i in paramlist:
        r_str = "${" + str(i) + "}"
        if valuepools.get(i) is not None:
            # obj = re.sub("\$\{"+str(i)+"\}", str(valuepools[i]), obj)
            obj = obj.replace(r_str, str(valuepools[i]))
        elif var.get(i) is not None:
            obj = obj.replace(r_str, str(var[i]))
        elif var.get(i) is not None and valuepools.get(i) is not None:
            obj = obj.replace(r_str, str(var[i]))
        else:
            print("var|valuePool中不存在需要的参数{}".format(i))
            raise NotFoundParams(i)
    return obj


# image转base64方法
def image_2_base64(path):
    with open(path, "rb") as f:
        base64_data = base64.b64encode(f.read())
        base64_data = str(base64_data, encoding="utf-8")
    return base64_data


def image_2_obj(path):
    """
    {
    "field1" : ("filename1", open("filePath1", "rb")),
    "field2" : ("filename2", open("filePath2", "rb"), "image/jpeg"),
    "field3" : ("filename3", open("filePath3", "rb"), "image/jpeg", {"refer" :"localhost"})
    }
    :param path: 
    :return: 
    """
    pass


# image转json
def image_2_json(filename, path):
    with open(path, 'rb') as f:
        return (filename, f, 'image/png')


def post_files(path):
    import mimetypes
    if os.path.isfile(str(path)):
        filename =path.split("/")[-1]
        mimetype = mimetypes.guess_type(filename)[0]
        return (filename, open(path, 'rb'), mimetype)


# ############################### 自定义扩展函数 ######################################


def collect_value(re, tp, str):
    if tp == "headers":
        headers = re.headers
        if str.upper() == "COOKIE":
            return headers["Set-Cookie"]
        elif str.upper() == "SESSION":
            pass
    pass


def get_value(*args, **kwargs):
    return 1


# 清理api测试后的参数环境
def clear_value(args):
    del(args)


# 随机生成数字
def get_random_num(min, max, len=None):
    """
    随机生成数字，在mix到max之间的任意数字
    :param min: 最小开始数字
    :param max: 最大结束数字
    :param len: 间隔多少取值
    :return: 数字
    """
    if len is None:
        result = random.randint(min, max)
    else:
        result = random.randrange(min, max, len)
    return result


# 随机生成字符串
def get_random_str(str, num=None):
    """
    随机生成字符串，在str中任意生成字符串
    :param str: 字符串
    :param num: 字符长度
    :return: 特定字符长度的随机字符串
    """
    if num is None:
        result = random.choice(str)
    else:
        result = random.sample(str, num)
        result = ''.join(result)
    return result


# 从一组中获取随机和指定值
def get_random_from_list(group, i=None):
    if i is None:
        h = len(group)
        i = get_random_num(0, h)
    return group[i]


# ############################### 数据库相关扩展函数 ####################################
def sql_select(sql, path, db=1, index=0):
    """
    从数据库中获取需要的值，目前仅支持返回单个值
    :param sql: 数据库执行的sql语句
    :param path: 获取数据库的链接配置
    :param db: 选择
    :return: 
    """
    pc = ParserConf(path)
    if db == 1:
        conf = {
            "host": pc.get_item("DB1", "host"),
            "port": pc.get_int_item("DB1", "port"),
            "user": pc.get_item("DB1", "user"),
            "password": pc.get_item("DB1", "password"),
            "db": pc.get_item("DB1", "db"),
            "charset": pc.get_item("DB1", "charset")
        }
    elif db == 2:
        conf = {
            "host": pc.get_item("DB2", "host"),
            "port": pc.get_int_item("DB2", "port"),
            "user": pc.get_item("DB2", "user"),
            "password": pc.get_item("DB2", "password"),
            "db": pc.get_item("DB2", "db"),
            "charset": pc.get_item("DB1", "charset")
        }
    try:
        conn = pymysql.connect(**conf)
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        result = cursor.fetchone()
    except Exception as e:
        print("sql执行错误,请检查sql exception: {}".format(e))
    cursor.close()
    conn.close()
    return result[index]






