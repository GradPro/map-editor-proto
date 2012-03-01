# -*- coding: UTF-8 -*-
from ConfigParser import DuplicateSectionError
from boto import config
from flaskapp import app

# 給boto設定要連線sdb的帳密和啟用加密連線
try:
    config.add_section('DB')
except DuplicateSectionError:
    pass
config.set('DB', 'db_user', app.config['AWS_ACCESS_KEY_ID'])
config.set('DB', 'db_passwd', app.config['AWS_SECRET_ACCESS_KEY'])
config.setbool('DB', 'enable_ssl', True)
