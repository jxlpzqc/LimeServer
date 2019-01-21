import datetime
import os

SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)

SQL_USERNAME = 'root'
SQL_PASSWORD = '6666'
SQL_HOSTADDRESS = 'localhost'
SQL_HOSTPORT = '3306'
SQL_DATABASE = 'lime'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (
	SQL_USERNAME, SQL_PASSWORD, SQL_HOSTADDRESS, SQL_HOSTPORT, SQL_DATABASE)
