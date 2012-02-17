# -*- coding: UTF-8 -*-
import logging, sys
import boto
from main import app

# 組態設定
import cfg
app.config.from_object(cfg)

# 設定 boto 偵錯模式
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
boto.config.set('Boto', 'debug', '1' if app.config.get('DEBUG') else '0')

# 網址對應 view functions
import urls

# 樣板設定
import tpl
