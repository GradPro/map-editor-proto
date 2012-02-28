# -*- coding: UTF-8 -*-
from flask import url_for
from jinja2 import Markup
from main import app

site = {
        'title': u'網頁遊戲',
        'desc' : u'HTML5 網頁戰略遊戲',
        'favicon': Markup('<link rel="shortcut icon" href="http://google.com/favicon.ico" />')
        }

nav = [
       {
        'title': u'首頁',
        'endpoint': 'home',
        },
       {
        'title': u'地圖',
        'sub': 'map',
        },
       ]

sub_nav = {
           'map': [
                   {
                    'title': u'地圖清單',
                    'endpoint': 'map.list',
                    },
                   {
                    'title': u'新增地圖',
                    'endpoint': 'map.add',
                    },
                   ]
           }

site['nav'] = nav
site['sub_nav'] = sub_nav

@app.context_processor
def inject_template_vars():
# 把site變數插入為預設樣板變數
    return dict(site=site)

css_libs = {
            'bootstrap': 'css/bootstrap.min.css',
            'main': 'css/main.css',
            }

def link_css(lib_name):
# http://jinja.pocoo.org/docs/api/#jinja2.Markup
# 一般在樣板引擎中，任何字串都會被跳脫成非html字元，例如 < > 這幾種字元會被轉換掉
# 是為了安全性考量，避免被插入惡意代碼，但如果是 Markup 就會照原樣輸出
# http://flask.pocoo.org/docs/api/#flask.url_for
    return Markup('<link rel="stylesheet" href="%s">' % \
                  url_for('static', filename=css_libs[lib_name]))

js_ex_libs = {
              'jQuery': 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js',
              }
js_libs = {
           'bootstrap': 'js/bootstrap.min.js',
           }

def link_ex_js(lib_name):
    return Markup('<script src="%s"></script>' % js_ex_libs[lib_name])

def link_js(lib_name):
    return Markup('<script src="%s"></script>' % \
                  url_for('static', filename=js_libs[lib_name]))

@app.context_processor
def register_template_functions():
    return dict(link_css=link_css, link_js=link_js, link_ex_js=link_ex_js)
