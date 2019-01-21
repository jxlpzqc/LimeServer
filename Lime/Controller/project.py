from datetime import datetime

from flask import *
from sqlalchemy import or_

from Lime.Handle.permission_check import authorize, has_permission
from ..app import *
from ..Model import *


@app.route('/project/newProject', methods=['POST'])
@authorize('NewProject')
def newProject():
    formData = request.get_json()
    name = formData['name']
    region = formData['region'][2]
    partyA = formData['partyA']
    partyB = formData['partyB']
    price = float(formData['price'])
    person = formData['person']
    phone = formData['phone']
    start_time = datetime.strptime(formData['during'][0][:10], "%Y-%m-%d")
    end_time = datetime.strptime(formData['during'][1][:10], "%Y-%m-%d")
    date = datetime.strptime(formData['date'][:10], "%Y-%m-%d")
    add_time = datetime.now()
    id = ''
    strprepend = str(datetime.now().year) + '' + str(datetime.now().month)
    maxProject = project.Project.query.filter(project.Project.id.like(strprepend + r"%")).order_by(
        project.Project.id.desc()).first()
    if maxProject is None:
        id = strprepend + '0001'
    else:
        id = str(int(maxProject.id) + 1) + ''
    newProjcet = project.Project(id, name, partyA, partyB, price, region, person, phone, session['username'], date,
                                 add_time, end_time, start_time)
    db.session.add(newProjcet)
    db.session.commit()
    ret = {'code': 0, 'msg': '创建成功！', 'data': {'id': id}}
    return json.dumps(ret)


@app.route('/project/myProject', methods=['POST'])
@authorize('NewProject')
def myProject():
    formData = request.get_json()
    pageNumber = formData['pageNumber']  # from 0 start
    searchText = formData['searchText']
    strSearch = "%" + searchText + "%"
    allProjectQuery = project.Project \
        .query.filter(project.Project.userid_add == session['username']).filter(
        or_(or_(or_(project.Project.projectname.like(strSearch), \
                    project.Project.partyAName.like(strSearch)), project.Project.person.like(strSearch)),
            project.Project.id.like(strSearch)))
    totalNum = allProjectQuery.count()

    allProject = allProjectQuery.slice(pageNumber * 10, (pageNumber + 1) * 10).all()
    ret = {'code': 0, 'msg': '查询成功', 'data': {'total': totalNum, 'data': []}}
    for x in allProject:
        item = {}
        item['id'] = x.id
        item['name'] = x.projectname
        item['partyA'] = x.partyAName
        item['partyB'] = x.partyBName
        item['price'] = x.price
        item['region'] = [x.region[0:2] + '0000', x.region[0:4] + '00', x.region]
        item['person'] = x.person
        item['date'] = x.date.strftime("%Y-%m-%d")
        item['during'] = [x.start_time.strftime("%Y-%m-%d"), x.end_time.strftime("%Y-%m-%d")]
        item['phone'] = x.phone
        now = datetime.now()

        if (now - x.add_time).total_seconds() < 24 * 60 * 60 or has_permission('EditProject'):
            item['editable'] = True
        else:
            item['editable'] = False
        ret['data']['data'].append(item)
    return json.dumps(ret)


@app.route('/project/deleteProject', methods=['POST'])
@authorize('NewProject')
def deleteProject():
    formData = request.get_json()
    deleteID = formData['id']
    isOk = False
    pro = project.Project.query.filter_by(id=deleteID).first()
    if has_permission("EditProject"):
        isOk = True
    elif (pro.userid_add == session['username']) \
            and ((datetime.now() - pro.add_time).total_seconds() < 24 * 60 * 60):
        idOk = True
    if isOk:
        db.session.delete(pro)
        db.session.commit()
        ret = {'code': 0, 'msg': "删除成功"}
    else:
        ret = {'code': -401, 'msg': '没有权限'}
    return json.dumps(ret)


@app.route('/project/updateProject', methods=['POST'])
@authorize('NewProject')
def updateProject():
    formData = request.get_json()
    id = formData['id']
    isOk = False
    pro = project.Project.query.filter_by(id=id).first()
    if has_permission('EditProject'):
        isOk = True
    elif (pro.userid_add == session['username']) \
            and ((datetime.now() - pro.add_time).total_seconds() < 24 * 60 * 60):
        idOk = True
    if isOk:
        pro.projectname = formData['name']
        pro.region = formData['region'][2]
        pro.partyAName = formData['partyA']
        pro.partyBName = formData['partyB']
        pro.price = float(formData['price'])
        pro.person = formData['person']
        pro.phone = formData['phone']
        pro.start_time = datetime.strptime(formData['during'][0], "%Y-%m-%d")
        pro.end_time = datetime.strptime(formData['during'][1], "%Y-%m-%d")
        pro.date = datetime.strptime(formData['date'], "%Y-%m-%d")
        db.session.commit()
        ret = {'code': 0, 'msg': "修改成功"}
    else:
        ret = {'code': -401, 'msg': '没有权限'}
    return json.dumps(ret)


@app.route('/project/allProject', methods=['POST'])
@authorize('ViewProject')
def allProject():
    formData = request.get_json()
    pageNumber = formData['pageNumber']  # from 0 start
    searchText = formData['searchText']
    strSearch = "%" + searchText + "%"
    allProjectQuery = project.Project \
        .query.filter(
        or_(or_(or_(project.Project.projectname.like(strSearch), \
                    project.Project.partyAName.like(strSearch)), project.Project.person.like(strSearch)), \
            project.Project.id.like(strSearch)))

    totalNum = allProjectQuery.count()

    allProject = allProjectQuery.slice(pageNumber * 10, (pageNumber + 1) * 10).all()
    ret = {'code': 0, 'msg': '查询成功', 'data': {'total': totalNum, 'data': []}}
    for x in allProject:
        item = {}
        item['id'] = x.id
        item['name'] = x.projectname
        item['partyA'] = x.partyAName
        item['partyB'] = x.partyBName
        item['price'] = x.price
        item['region'] = [x.region[0:2] + '0000', x.region[0:4] + '00', x.region]
        item['person'] = x.person
        item['date'] = x.date.strftime("%Y-%m-%d")
        item['during'] = [x.start_time.strftime("%Y-%m-%d"), x.end_time.strftime("%Y-%m-%d")]
        item['phone'] = x.phone
        now = datetime.now()

        if (now - x.add_time).total_seconds() < 24 * 60 * 60 or has_permission('EditProject'):
            item['editable'] = True
        else:
            item['editable'] = False
        ret['data']['data'].append(item)
    return json.dumps(ret)
