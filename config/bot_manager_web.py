import os
from .__bot__ import HOST, PORT

# 显示ICP备案相关的内容，如果没有ICP备案信息要显示的话保持为空就可以了
ICP_CONTENT = ''
# 私聊机器人“bot设置”返回的网址基础域名，默认是从hoshino的配置中读取
PUBLIC_ADDRESS = f"http://{HOST}:{PORT}"
# 访问bot manager web的密码。公网服务没有身份验证是很危险的，密码建议自行修改！！！
PASSWORD = '987654321'
