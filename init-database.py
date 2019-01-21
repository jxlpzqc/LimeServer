from datetime import datetime

from Lime.app import *
from Lime.Model import *

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    newG = user.Group("admin", "['all']")
    newG2 = user.Group("user", "['NewProject']")
    newUser = user.User("admin", "1", "111", None, None, "admin")
    newUser2 = user.User("user", "1", "111", None, None, "user")
    pro = project.Project("2019010001", "小项目", "乐平政府", "LP", 100000, "360281", "小明", \
                          "13801010101", "user", datetime.strptime("2019-01-01", "%Y-%m-%d"),
                          datetime.strptime("2019-01-01", "%Y-%m-%d"), \
                          datetime.strptime("2019-01-01", "%Y-%m-%d"), datetime.strptime("2019-01-24", "%Y-%m-%d"))

    db.session.add(newG)
    db.session.add(newG2)
    db.session.add(newUser)
    db.session.add(newUser2)
    db.session.add(pro)
    db.session.commit()
