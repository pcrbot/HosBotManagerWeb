import os
import json
import nonebot
from datetime import timedelta
from hoshino import Service
from quart import request, session, redirect, Blueprint
from .http_handler import render_template, get_random_str

# 访问bot manager web的密码。公网服务没有身份验证是很危险的，密码建议自行修改！！！
PASSWORD = os.environ.get('BOT_MANAGER_WEB_PASSWORD') if os.environ.get('BOT_MANAGER_WEB_PASSWORD') else '987654321'

switcher = Blueprint('switcher', __name__, static_folder='statics', static_url_path='/statics', url_prefix="/manage")
bot = nonebot.get_bot()
app = bot.server_app
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = get_random_str(10)


async def get_groups():
    return await bot.get_group_list()


@switcher.before_request
async def _():
    user_ip = request.remote_addr
    if session.get('user_ip') == user_ip:
        return
    if request.path.startswith(switcher.url_prefix):
        r_path = request.path[len(switcher.url_prefix):]
        if r_path == '/login':
            return
        if r_path.startswith(switcher.static_url_path):
            return
        if r_path == '/check':
            return
        return redirect(switcher.url_prefix + '/login')


@switcher.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'GET':
        return await render_template('login.html', title='登录', static_url_path=switcher.static_url_path,
                                     url_prefix=switcher.url_prefix)
    else:
        login_data = await request.form
        input_psd = login_data.get('password')
        if input_psd == PASSWORD:
            user_ip = request.remote_addr
            session['user_ip'] = user_ip
            session.permanent = True
            app.permanent_session_lifetime = timedelta(weeks=2)
            return redirect(switcher.url_prefix + '/')
        else:
            return redirect(switcher.url_prefix + '/login')


@switcher.route('/')
async def manage():
    user = {'name': 'name'}
    return await render_template('manage.html', title='欢迎', user=user, static_url_path=switcher.static_url_path,
                                 url_prefix=switcher.url_prefix)


@switcher.route('/group')
async def group_list():
    user = {'name': 'name'}
    groups = await get_groups()
    return await render_template('group_list.html', title='按群管理', article_title="按群管理", items=groups, user=user,
                                 static_url_path=switcher.static_url_path, url_prefix=switcher.url_prefix)


@switcher.route('/service')
async def service_list():
    user = {'name': 'name'}
    svs = Service.get_loaded_services()
    sv_names = list(svs)
    return await render_template('service_list.html', title='按服务管理', article_title="按服务管理", items=sv_names, user=user,
                                 static_url_path=switcher.static_url_path, url_prefix=switcher.url_prefix)


@switcher.route('/group/<gid_str>')
async def show_group_services(gid_str: str):
    user = {'name': 'name'}
    gid = int(gid_str)
    svs = Service.get_loaded_services()
    conf = {gid_str: {}}
    for key in svs:
        conf[gid_str][key] = svs[key].check_enabled(gid)
    return await render_template('group_services.html', title=f'群{gid_str}服务一览', article_title=f'群{gid_str}服务一览',
                                 user=user, group_id=gid_str, conf=conf, static_url_path=switcher.static_url_path,
                                 url_prefix=switcher.url_prefix)


@switcher.route('/service/<sv_name>')
async def show_service_groups(sv_name: str):
    user = {'name': 'name'}
    svs = Service.get_loaded_services()
    groups = await get_groups()
    conf = {}
    for group in groups:
        gid = group['group_id']
        gid_str = str(gid)
        conf[gid_str] = {}
        if svs[sv_name].check_enabled(gid):
            conf[gid_str][sv_name] = True
        else:
            conf[gid_str][sv_name] = False
    return await render_template('service_groups.html', title=f'服务 {sv_name} ', article_title=sv_name, sv_name=sv_name,
                                 conf=conf, groups=groups, user=user, static_url_path=switcher.static_url_path,
                                 url_prefix=switcher.url_prefix)


@switcher.route('/set', methods=['GET', 'POST'])
async def set_group():
    # 接收前端传来的配置数据，数据格式{"<gid>":{'serviceA':True,'serviceB':False}}
    if request.method == 'POST':
        data = await request.get_data()
        conf = json.loads(data.decode())
        svs = Service.get_loaded_services()
        for k in conf:
            gid = int(k)
            for sv_name in conf[k]:
                if conf[k][sv_name]:
                    svs[sv_name].set_enable(gid)
                    svs[sv_name].logger.info(f'启用群 {gid} 服务 {sv_name} ')
                else:
                    svs[sv_name].set_disable(gid)
                    svs[sv_name].logger.info(f'禁用群 {gid} 服务 {sv_name}')
        return 'ok'
