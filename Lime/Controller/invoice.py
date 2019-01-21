from datetime import datetime

from flask import *
from sqlalchemy import or_

from Lime.Handle.permission_check import authorize, has_permission
from ..app import *
from ..Model import *


@app.route('/invoice/newInvoice',methods=['POST'])
@authorize('NewInvoice')
def newInvoice():
    formData = request.get_json()
    id = formData['id']
    projectId = formData['projectId']
    partyB = formData['partyB']
    sum = float(formData['sum'])
    rate = float(formData['rate'])
    cash = float(formData['cash'])
    card = float(formData['card'])
    ps = formData['ps']
    price = sum / (1 + rate)
    tax = sum - price
    newInv = invoice.Invoice(id, projectId, partyB, sum, rate, price, tax, cash, card, ps)
    db.session.add(newInv)
    db.session.commit()
    ret = {'code': 0, 'msg': '添加成功'}
    return json.dumps(ret)
