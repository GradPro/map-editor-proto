# -*- coding: UTF-8 -*-
import logging, sys
from ConfigParser import DuplicateSectionError
import boto
from main import app

# 組態設定
import cfg
app.config.from_object(cfg)

if app.config.get('DEBUG'):
    to_cmd = logging.StreamHandler(stream=sys.stdout)
    to_cmd.setFormatter(fmt=logging.Formatter(fmt='%(message)s\n' +'='*100))
    werkzeug_logger = logging.getLogger(name='werkzeug')
    werkzeug_logger.addHandler(hdlr=to_cmd)
    werkzeug_logger.setLevel(logging.DEBUG)

    from prefix_filter import PrefixFilter
    prefix = ['using', 'string_to_sign:', 'len(b64)', 'base64', 'query_string:',
              'StringToSign:',
              ]
    to_cmd = logging.StreamHandler(stream=PrefixFilter(prefix))
    to_cmd.setFormatter(fmt=logging.Formatter(fmt='%(message)s\n' +'-'*150))
    boto_logger = logging.getLogger(name='boto')
    boto_logger.addHandler(hdlr=to_cmd)
    boto_logger.setLevel(logging.DEBUG)

# 設定 boto 偵錯模式
try:
    boto.config.add_section('Boto')
except DuplicateSectionError:
    pass
boto.config.set('Boto', 'debug', '2' if app.config.get('DEBUG') else '0')

# 網址對應 view functions
import urls

# 樣板設定
import tpl
