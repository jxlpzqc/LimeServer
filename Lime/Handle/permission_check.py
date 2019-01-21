import json
from functools import wraps

from flask import session


def authorize(permission):

	def auth(func):
		@wraps(func)
		def wrapper(*args, **kwargs):

			if ('username' in session.keys()
					and not session['username'] is None
					and session['username'] != ''
					and ('all' in session['permission'] or permission in session['permission'])):

				return func(*args, **kwargs)
			else:
				if not ('username' in session.keys()
					and not session['username'] is None
					and session['username'] != ''):
					ret = {'code':'-400','msg':'未登录'}
				else:
					ret = {'code':'-401','msg':'权限不足'}
				return json.dumps(ret)

		return wrapper
	return auth


def has_permission(permission):
	if 'all' in session['permission']:
		return True
	elif permission in session['permission']:
		return True
	else:
		return False


