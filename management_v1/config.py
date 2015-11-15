__author__ = 'med'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True

SECRET_KEY = 'GWPviGUK2Q232nHOmM4xMqfxo84x9L0NuUO9L5We'


USER_AUTH_URL = 'http://controller:5000/v2.0'

ADMIN_TENANT_NAME = 'admin'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'
ADMIN_AUTH_URL = 'http://controller:35357/v2.0'


HOST = 'http://controller:8080'

UPLOAD_FOLDER = '/tmp'
