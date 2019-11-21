# ApiTestForHttp
一款用于测试部门协作进行接口测试的小框架，主要适用于冒烟测试和回归测试，支持单接口和多接口场景流程测试,目前他支持一下相关功能：
1. 支持json文件内部的参数化操作
2. 支持自定义方法并在json文件中参数化引用
3. 支持log的自动生成和输出
4. 支持report的自动生成和输入
5. 支持api请求失败重连原则
6. 支持命令行模式下运行脚本
7. 支持api单接口以及业务流程场景测试

####项目目录篇：
![image.png](https://upload-images.jianshu.io/upload_images/17968751-46258ca4d5d48c53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如上图所示主要包含以下结构和内容
1. project  项目根目录
2. InitConf.ini   项目配置文件
3. test_xxxxx.json  实际的测试json文件
**一般情况下，登录成功的脚本case一般需要放置在project的目录下，这样可以优先登录成功并提取相关登录信息给其他依赖权限的接口使用**

####初始化配置篇
![image.png](https://upload-images.jianshu.io/upload_images/17968751-16ca3286fee9a62d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
1. 如果存在多数据库，需要在配置文件中，如上图所示按照DB1 DB2 DB3来进行设置

####json编写篇
```
     {
     "name": "login_commuity_with_jack_中文",
     "setup": {
        "num1": 123,
        "str1": "anc",
        "fun1": "${__get_value(a=1, b=2)}",
        "fun2": "${__get_value('success')}",
        "str2": "jack2${str1}",
        "fun3": "${__get_value(${num1}, '${str1}', '${str2}')}",   # 注意1  方法参数化如果入参是字符串，需要加两个单引号
        "path": "E:\\jackstudy\\test\\test_params.py",
        "dict": {"a":"${str1}"},
        "dict-list": {
          "c" : "-${num1}" ,   # 注意2  对于字典或者列表中某一个value需要获取某一个int值转为str类型显示时，在前面加“-” or “~”
          "a": "${num1}", # 注意4 对于字段为非确定数据类型， a会获取num1的自带int类型，b会自动获取str1中的str类型
          "b": "${str1}",
          "c": "abc${num1}",
          "areaCodes": ["${num1}","${str1}","abc${num1}"],
          "street": {"aa": "${num1}","bb": "${str1}"}
        },
        "list": ["A${num1}", 2]            # 注意3  对于字典或者列表中某一个value中部分需要获取某一个int值转为str类型显示，框架会自动判断进行合并

     },

     "requestor":{
        "url": "${host}/mccemv/mgr/api/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
       "data": "${dict-list}",
       "files":{"image":"${path}"}
     },

     "validator": {
       "assertEqCode": 299,
       "assertEqHeaders": {"Content-Type": "application/json;charset=UTF-8"},
       "assertEqStr": ["100000"],
       "assertEqJson":{"success":true}
     },

     "collector":{
       "json": {"token": "response.data.token"},
       "methods": {"deleteid": "${__sql_select('${sql}', '${confpath}')}"},
       "values":{"deleteid2": "${num1}"}
     },

     "teardown":{
       "clear_cookies": "clearcookies",
       "clearsession": "clearsession",
       "cleartoken": "cleartoken"
     }
   }
```
> 参数化原则：
1 对于参数化后非确定类型，必须进行类型转换时， 需要在参数化标记$前增加一个“”-“” - **参考注意2**
2 对于字典或者列表字段为str类型时，不需要做类型转换，框架会自动完成 - **参考注意3**
3 对于字典或者列表中字段值为非确定数据类型，参数会保留参数化字段的原有type进行替换 - **参考注意4**
4 对于方法类的str类型进行参数化时，需要人工确定传值是数值还是字符串，如果是字符串需要人工增加单引号 - **参考注意1**

####框架执行篇
#####命令行模式
![image.png](https://upload-images.jianshu.io/upload_images/17968751-2b4e4a46ef6379fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行整个项目: **python3 api_test.py -p E:\jackstudy\ApiTestForHttp\data\project**

执行单个文件：**python3 api_test.py -p E:\test_.json -cf E:\data\conf**

####报告生成篇
通过命令行执行报告后，查看执行窗口报告生成情况，如下图
![image.png](https://upload-images.jianshu.io/upload_images/17968751-fab8af09e36a2dfe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

框架report目录下报告如下：
![image.png](https://upload-images.jianshu.io/upload_images/17968751-4a4086ae66d5d51c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



>欢迎各位体验，体验入口：[https://github.com/jackyin2/ApiTestForHttp](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjackyin2%2FApiTestForHttp)



  


