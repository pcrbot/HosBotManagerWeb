import os
import nonebot
from hoshino.config import HOST, PORT

# 私聊机器人“bot设置”返回的网址基础域名，默认是从hoshino的配置中读取
PUBLIC_ADDRESS = os.environ.get('PUBLIC_ADDRESS') if os.environ.get('PUBLIC_ADDRESS') else f"http://{HOST}:{PORT}"

bot = nonebot.get_bot()


@bot.on_message('private')
async def setting(ctx):
    message = ctx['raw_message']
    if message == 'bot设置':
        await bot.send(ctx, f'{PUBLIC_ADDRESS}/manage', at_sender=False)
