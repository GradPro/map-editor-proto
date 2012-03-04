# -*- coding: UTF-8 -*-
import gevent.monkey
# 安裝gevent到標準函式庫
gevent.monkey.patch_all()
from wsgi import app

def main():
    # http://flask.pocoo.org/docs/api/#flask.Flask.run
    app.run(host="0.0.0.0", port=80)

if __name__ == '__main__':
# 被直接執行而不是被import的話，__name__就會是 '__main__'
# 如果是被import的話，就會是 module 的名字，例如 abc.py 這個 module 的名字就是 abc
    main()
