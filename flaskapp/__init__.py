# -*- coding: UTF-8 -*-
import logging, sys
from ConfigParser import DuplicateSectionError
import boto
from main import app

# 組態設定
# http://flask.pocoo.org/docs/api/#flask.Config.from_object
import cfg
app.config.from_object(cfg)

# 如果組態中，DEBUG有被設定
if app.config.get('DEBUG'):
    # 印到stdout (就是命令列)的log處理器
    to_cmd = logging.StreamHandler(stream=sys.stdout)
    # 每一行log下面加上一行100個等號的分隔線，方便閱讀
    to_cmd.setFormatter(fmt=logging.Formatter(fmt='%(message)s\n' +'='*100))
    # flask用的wsgi環境函式庫用的logger
    werkzeug_logger = logging.getLogger(name='werkzeug')
    werkzeug_logger.addHandler(hdlr=to_cmd)
    # 等級比debug高的都會收錄，log等級低到高：debug, info, warning, error, critical
    werkzeug_logger.setLevel(logging.DEBUG)

    # 自己寫的過濾器，因為boto的log太囉嗦了
    from prefix_filter import PrefixFilter
    # log如果是這些開頭的，就不會被印出來
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
