from ..app import db

class User(db.Model):
	username = db.Column(db.String(50), primary_key=True)
	password = db.Column(db.String(50))
	nickname = db.Column(db.String(50), nullable=True)
	avator = db.Column(db.Text, nullable=True)
	depart = db.Column(db.String(50), nullable=True)
	group_id = db.Column(db.String(50), db.ForeignKey("group.groupname"))
	def __init__(self,username,password,nickname,avator,depart,group_id):
		self.username = username;
		self.password = password;
		self.nickname = nickname;
		self.avator = avator;
		self.depart = depart;
		self.group_id = group_id;

class Group(db.Model):
	groupname = db.Column(db.String(50), primary_key=True)
	permission = db.Column(db.Text)

	user = db.relationship("User", backref="group")
	def __init__(self,groupname,permission):
		self.groupname = groupname
		self.permission = permission