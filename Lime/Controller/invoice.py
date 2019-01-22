from datetime import datetime

from flask import *
from sqlalchemy import or_

from Lime.Handle.permission_check import authorize, has_permission
from ..app import *
from ..Model import *


@app.route('/invoice/newInvoice', methods=['POST'])
@authorize('NewInvoice')
def newInvoice():
    formData = request.get_json()
    id = formData['id']
    projectId = formData['projectId']
    partyB = formData['partyB']
    sum = round(float(formData['sum']), 2)
    rate = float(formData['rate'])

    cash = round(float(formData['cash']), 2)
    card = round(float(formData['card']), 2)
    taxarrive_sum = cash + card

    ps = formData['ps']
    price = round(sum / (1 + rate), 2)
    tax = round(sum - price, 2)
    if invoice.Invoice.query.filter_by(id=id).count() > 0:
        ret = {'code': -1, 'msg': '已经存在这个发票!'}
        return json.dumps(ret)

    newInv = invoice.Invoice(id, projectId, partyB, sum, rate, price, tax, taxarrive_sum, ps, datetime.now(),
                             session['username'])

    newTaCash = invoice.TaxArrive()
    newTaCash.invoiceID = id
    newTaCash.method = 0
    newTaCash.time = datetime.now()
    newTaCash.money = cash

    newTaCard = invoice.TaxArrive()
    newTaCard.invoiceID = id
    newTaCard.method = 0
    newTaCard.time = datetime.now()
    newTaCard.money = card

    db.session.add(newInv)
    db.session.commit()
    db.session.add(newTaCash)
    db.session.add(newTaCard)
    db.session.commit()

    ret = {'code': 0, 'msg': '添加成功'}
    return json.dumps(ret)


@app.route("/invoice/getInvoice", methods=['POST'])
@authorize("ViewInvoice")
def getInvoice():
    formData = request.get_json()
    pageNumber = formData['pageNumber']  # from 0 start
    searchText = formData['searchText']
    projectID = formData['projectID']
    strSearch = "%" + searchText + "%"

    allInvoiceQuery = invoice.Invoice.query.filter(invoice.Invoice.projectID.like(projectID)).filter(
        invoice.Invoice.id.like(strSearch))
    totalNum = allInvoiceQuery.count()

    allInvoice = allInvoiceQuery.slice(pageNumber * 10, (pageNumber + 1) * 10).all()
    ret = {'code': 0, 'msg': '查询成功', 'data': {'total': totalNum, 'data': []}}
    for x in allInvoice:
        item = {}
        item['id'] = x.id
        item['projectID'] = x.projectID
        item['projectName'] = x.project.projectname
        item['partyA'] = x.project.partyAName
        item['person'] = x.project.person
        item['partyB'] = x.partyB
        item['sum'] = x.sum
        item['rate'] = x.rate
        item['price'] = x.price
        item['tax'] = x.tax
        item['taxarrive'] = x.taxarrive_sum
        item['ps'] = x.ps

        item['time'] = x.add_time.strftime("%Y-%m-%d %H:%M:%S")
        # item['add_time'] = x.add_time
        # item['userid_add'] = x.userid_add
        item['arrive'] = x.arrive_sum
        now = datetime.now()

        if (now - x.add_time).total_seconds() < 24 * 60 * 60 or has_permission('EditInvoice'):
            item['editable'] = True
        else:
            item['editable'] = False
        ret['data']['data'].append(item)
    return json.dumps(ret)
