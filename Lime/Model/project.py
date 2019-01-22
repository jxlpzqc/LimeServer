from ..app import db

class Project(db.Model):
    id = db.Column(db.String(20),primary_key=True)
    projectname = db.Column(db.String(50))
    partyAName = db.Column(db.String(50))
    partyBName = db.Column(db.String(50))
    price = db.Column(db.REAL)
    region = db.Column(db.String(50))
    person = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    date = db.Column(db.Date)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)

    add_time = db.Column(db.DateTime)
    userid_add = db.Column(db.String(50),db.ForeignKey("user.username"))
    user_add = db.relationship("User", backref="project")

    def __init__(self, id, projectname, partyAName, partyBName, price, region, person, phone, userid_add, date,
                 add_time, end_time, start_time):
        self.id = id
        self.projectname = projectname
        self.partyAName = partyAName
        self.partyBName = partyBName
        self.price = price
        self.region = region
        self.person = person
        self.phone = phone
        self.date = date
        self.add_time = add_time
        self.userid_add = userid_add
        self.start_time = start_time
        self.end_time = end_time