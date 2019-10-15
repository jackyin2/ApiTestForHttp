# ApiTestForHttp
一款用于测试部门协作进行接口测试的小框架，主要适用于冒烟测试和回归测试，支持单接口和多接口场景流程测试


**前言**

个人一个普通的测试人员，一直在从事业务测试和项目管理方面的工作，随着时代的发展，测试这个职业也在快速升级中，更高的要求也在激励着我往更深一层次去发展，锻炼自己开发这个脚本框架目的只有一个，我没有那么高的职业理想，仅仅希望自己不被市场淘汰，也许不完美，但是我努力过，所以基于公司的前后端分离项目为背景，我尝试开发了一套接口测试框架
 
**1 框架简介**
 
本框架是基于py3进行开发，功能方面目前主要解决的是前后端分离框架下的普通http协议的接口相关的测试。
    
**2 设计思路**
 
1. 首先设计的灵感是基于unittest的框架的case管理方式

2. 其次基于jmeter中的提取器和验证器的设计思路

3. debugtalk大神的json、yaml的管理方式

当然（小私心就是锻炼锻炼自己的代码能力，虽然不咋地）

**功能介绍**

    1. 支持参数化（参数， 方法，方法入参），
    2. 支持自定义方法
    3. 支持接口的返回验证及结果自动提取
    4. 支持自定义错误异常的收集和返回
    5. 支持命令行执行
    6. 支持api测试报告的自动生成和结果统计
    7. 支持http协议下常用（get， post， patch，Put，delete）

**测试样本**
```
{
   "test": [{
     "name": "login_commuity_with_jack_中文",

     "setup": {
       "num1": 123,
        "str1": "anc",
        "fun1": "${__get_value(a=1, b=2)}",
        "fun2": "${__get_value('success')}",
        "str2": "jack2${str1}",
        "fun3": "${__get_value(${num1}, ${str1}, '${str2}')}",
        "path": "E:\\jackstudy\\test\\test_params.py",
        "dict": {"a":"${str1}"},
        "dict-list": {
          "a": "${num1}",
          "b": "${str1}",
          "c": "abc${num1}",
          "areaCodes": ["${num1}","${str1}","abc${num1}"],
          "street": {"aa": "${num1}","bb": "${str1}"},
        },
        "list": ["A${num1}", 2]
     },

     "requestor":{
        "url": "${host}/mccemv/device-mgr/api/auth/login",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
       },
        "data": { "username": "${username}", "password": "111111"},
        "files":{
            "image1":"path",
            "image2":"path2"
        }
     },

     "validator": {
       "assertEqCode": 299,
       "assertEqHeaders": {"Content-Type": "application/json;charset=UTF-8"},
       "assertEqStr": ["100000"],
       "assertEqJson":{"success":true}
     },

     "collector":{
       "json": {"token": "response.data.token"},
       "methods": {"deleteid": "${__sql_select('${sql}', '${confpath}')}"}
     },

     "teardown":{
       "clear_cookies": "clearcookies",
       "clearsession": "clearsession",
       "cleartoken": "cleartoken"
     }
   }]
}

简单谈下各部分的意义：
"test": 表示的时当前为一个需要测试的用例或者用例列表
"name": 本次测试用例用例的功能描述
"setup": 预设case执行前的预设条件
"requestor": api的主要核心部分
"validator": 检验器，用例case的执行完毕后结构校验
"collector": 收集器，主要针对将结果中重要信息回收给其他用例使用
"teardown": 回收，主要是销毁setup中的相关内容，减少垃圾
```
目前支持的方法（可自定义）：
      
    1. get_random_num(min, max, len=None) 任意生成随机数字
    2. get_random_str(str, num=None) 从str中任意字符随机组合num长度新字符
    3. sql_select(sql, path,  db=1)  同执行conf文件中，执行sql，获取单个值

case编写注意事项：

1. 目前case仅支持json文件格式，不支持yaml等

2. setupcase中，定义的参数化需要按照直接赋值 < 方法赋值（不带入参参数化） < 方法赋值（带入参参数化）的顺序进行编写

3. setupcase中，入参需要参数化的方法，如果入参是一个str类型，那么需要加上单引号

4. 项目结构必须按照：
    ![Image 项目结构](./templeate/static/QQ截图20190917101143.jpg)

5. 用例命名规范 可参考unittest的方式，test_id_method_desc_other.json

暂不支持：

```
1. 缺少log文件的输出，只能通过控制台查看执行过程
```

**如何开始？**

1. 新建项目结构

    在本地任意目录结构下新建如下图的项目
    
    ![Image 项目结构](./templeate/static/QQ截图20190917101143.jpg)
    
    新建项目中必须将logincase放置在项目节点下，同时同级中新建InitConf.ini配置文件

2. 编写case json文件，可参考案例

3. 编写用例后，可以进行单json调试：

    使用命令 python let_api.py -d 当前项目的路径 -f json文件路径 -r 生成report的名称(默认自动生成如果希望结果覆盖可填写) -c 是否加载配置文件（1/0）
    
    eg： python3 let_api.py -d E:\jackstudy\LetApiRun\data\custemor -f E:\jackstudy\LetApiRun\data\custem
or\superadmin\小区管理\数据看板\test_post_查询小区功能.json -r apireport.html -c 1


4. 单文件调试成功后，进行项目整体执行

    使用命令 python let_api.py -d 当前项目的路径
    
5. 查看报告
    
    report文件下查看report.html文件
    ![Image 项目结构](./templeate/static/report.jpg)
