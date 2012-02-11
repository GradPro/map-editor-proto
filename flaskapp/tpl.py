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
    return dict(site=site)

css_libs = {
            'bootstrap': 'css/bootstrap.min.css',
            'main': 'css/main.css',
            }

def link_css(lib_name):
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
