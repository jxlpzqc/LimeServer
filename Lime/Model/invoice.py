from ..app import db


class Invoice(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    projectID = db.Column(db.String(20), db.ForeignKey("project.id"))
    partyB = db.Column(db.String(20))
    sum = db.Column(db.REAL)
    rate = db.Column(db.REAL)
    price = db.Column(db.REAL)
    tax = db.Column(db.REAL)
    # cash = db.Column(db.Float)
    # card = db.Column(db.Float)
    taxarrive_sum = db.Column(db.REAL)
    ps = db.Column(db.Text)

    arrive_sum = db.Column(db.Float)

    add_time = db.Column(db.DateTime)
    userid_add = db.Column(db.String(50), db.ForeignKey("user.username"))
    user_add = db.relationship("User", backref="invoice")

    project = db.relationship("Project", backref='invoice')

    def __init__(self, id, projectID, partyB, sum, rate, price, tax, taxarrive_sum, ps, add_time, userid_add):
        self.id = id
        self.projectID = projectID
        self.partyB = partyB
        self.sum = sum
        self.rate = rate
        self.price = price
        self.tax = tax
        self.taxarrive_sum = taxarrive_sum
        self.ps = ps
        self.add_time = add_time
        self.userid_add = userid_add
        self.arrive_sum = 0


class TaxArrive(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    invoiceID = db.Column(db.String(20), db.ForeignKey("invoice.id"))
    invoice = db.relationship("Invoice", backref='taxarrive')

    method = db.Column(db.Integer)  # 0 现金 1 刷卡 2 扣款
    money = db.Column(db.REAL)
    time = db.Column(db.DateTime)


class Arrive(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    invoiceID = db.Column(db.String(20), db.ForeignKey("invoice.id"))
    invoice = db.relationship("Invoice", backref='arrive')

    money = db.Column(db.REAL)
    time = db.Column(db.DateTime)
