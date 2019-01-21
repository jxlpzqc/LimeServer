from ..app import db


class Invoice(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    projectID = db.Column(db.String(20), db.ForeignKey("project.id"))
    partyB = db.Column(db.String(20))
    sum = db.Column(db.Float)
    rate = db.Column(db.Float)
    price = db.Column(db.Float)
    tax = db.Column(db.Float)
    cash = db.Column(db.Float)
    card = db.Column(db.Float)
    ps = db.Column(db.Text)

    add_time = db.Column(db.DateTime)
    userid_add = db.Column(db.String(50),db.ForeignKey("user.username"))
    user_add = db.relationship("User", backref="invoice")

    project = db.relationship("Project", backref='invoice')

    def __init__(self,id,projectID,partyB,sum,rate,price,tax,cash,card,ps,add_time,userid_add):
        self.id = id
        self.projectID = projectID
        self.partyB = partyB
        self.sum = sum
        self.rate = rate
        self.price = price
        self.tax = tax
        self.cash = cash
        self.card = card
        self.ps = ps
        self.add_time = add_time
        self.userid_add = userid_add