from flask import *
from Lime.Handle.permission_check import authorize
from ..app import *
from ..Model import *


@app.route('/user/login', methods=['GET', "POST"])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    res = user.User.query.filter_by(username=username, password=password).first()
    if not res is None:
        permission = json.dumps(res.group.permission)
        session['username'] = username
        session['password'] = password
        session['permission'] = permission
        return json.dumps({'code': '0', 'msg': '登录成功', 'data': {'username': username, 'permission': permission}})
    else:
        return json.dumps({'code': '-1', 'msg': '用户名或密码错误'})

@app.route('/user/checkStatus',methods=['POST'])
def checkStatus():
    if('username' in session.keys() and session['username'] is not None and session['username'] != ''):
        return json.dumps({'code': '0', 'msg': '已登录', 'data': {'username': session['username'], 'permission': session['permission']}})
    else:
        return json.dumps({'code': '-1', 'msg': '未登录'})