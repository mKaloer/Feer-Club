from __future__ import absolute_import # optional, but I like it
from .common import *

with open('/home/django/Feer-Club/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()
DEBUG = False
ALLOWED_HOSTS = ['*']
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
