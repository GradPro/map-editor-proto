# -*- coding: UTF-8 -*-
from flask import Flask

#初始化 Web APP
app = Flask(__name__)

sitemap = [
           {
            'name': 'home',
            'title': u'首頁',
            'endpoint': 'home',
            },
           {
            'name': 'map',
            'title': u'地圖',
            'child': [
                      {
                       'name': 'map.list',
                       'title': u'地圖清單',
                       'endpoint': 'map_list',
                       },
                      {
                       'name': 'map.add',
                       'title': u'新增地圖',
                       'endpoint': 'map_add',
                       },
                      ]
            },
           ]
