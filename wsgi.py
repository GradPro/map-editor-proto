# -*- coding: UTF-8 -*-
import sys
import os.path as path

# sys.path 為python在import時，尋找對應module或package的路徑
# http://docs.python.org/library/sys.html#sys.path
# __file__ 變數為目前module的完整路徑，用path.dirname可取出資料夾路徑的部分
sys.path.append(path.dirname(__file__) + '/.lib')

import flaskapp
app = flaskapp.app
