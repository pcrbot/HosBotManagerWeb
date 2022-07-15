# 简介

基于一个叫[hoshinoV2服务开关网页版.zip](https://github.com/pcrbot/plugins-for-Hoshino/tree/master/shebot/webServiceManager)(作者 @shewinder ) 改出来的玩意儿，web管理hoshino的service开关的东西。 

## 安装

1. 前略装好hoshinobot。步骤参考[hoshino文档](https://github.com/Ice-Cirno/HoshinoBot)。

2. 整个`bot_manager_web`目录塞进`hoshino/modules`目录下面。

3. 在`hoshino/config/__bot__.py`文件中添加模块引用。MODULES_ON 这个字典中添加一行`'bot_manager_web'`。

4. 修改配置信息（密码请务必修改，避免造成信息泄露！）

BOT_MANAGER_WEB_PASSWORD

- 环境变量。环境变量中`BOT_MANAGER_WEB_PASSWORD`值设置为想要的密码。
- 如果不想用环境变量，则可以修改`hoshino/modules/bot_manager_web/view.py`中的`PASSWORD`后面值修改成你想要的密码。

PUBLIC_ADDRESS

这个一般不用管，直接引用的hoshino的配置。如果要修改的话

- 环境变量。环境变量中`PUBLIC_ADDRESS`值设置为想要的密码。
- 如果不想用环境变量，则可以修改`hoshino/modules/bot_manager_web/reply.py`中的`PUBLIC_ADDRESS`后面值修改成你想要的url。

## 使用

访问`https://bcr.yourdomain.com:<your port>/manage`

输入上面文件里设定的密码登录（至于为啥没有用户名，反正只有一个人会去登录的东西要什么用户名！）

然后是进入服务里管理群功能开关，还是进入群列表管理服务功能开关，正常人都能看懂吧。

PS: 注销按钮我也不知道为啥要存在，想了想也没啥意义就没做了。

PPS: 还有部分垃圾文件懒得看了，体积也不算太过夸张懒得抽了，有人有空可以抽一抽。

PPPS：友情提示！使用云服务器请确认对应端口在云服务器中是否开放！使用windows服务器请在服务器的防火墙中确认对应端口是否开放！

PPPPS: 端口请查看你的hoshine的文件 ```config/__bot__.py``` 里的PORT参数设置的是多少。

## 图示

![图1](Thumbnail/1.png)
![图2](Thumbnail/2.png)
![图3](Thumbnail/3.png)
![图4](Thumbnail/4.png)
![图5](Thumbnail/5.png)
