# -*- coding: UTF-8 -*-
import boto
from main import app

# 組態設定
import cfg
app.config.from_object(cfg)
boto.config.set('Boto', 'debug', '2' if app.config.get('DEBUG') else '0')

# 網址對應 view functions
import urls

# 樣板設定
import tpl
