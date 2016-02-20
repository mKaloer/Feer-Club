from __future__ import absolute_import # optional, but I like it
from .common import *

with open('/home/django/Feer-Club/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()
DEBUG = False
ALLOWED_HOSTS = ['*']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
