# -*- coding: UTF-8 -*-
import json
from flask import render_template, request, redirect, url_for
from flaskapp.model.maps import GameMap

def map_list():
    maps = GameMap.all()
    return render_template('map_list.html', maps=maps)

def map_editor(mid=None):
    #將map存於SDB
    if request.method == 'POST':
        map_data = json.loads(request.form.get('map'))
        if mid:
            map_item = GameMap.get_by_id('map_'+str(mid))
            map_item.name = request.form.get('name')
            map_item.grid = json.dumps(map_data['grid'])
            if not map_item.name: map_item.name = '無標題'
            map_item.save()
            return redirect(url_for('map.list'))
        else:
            map_item = GameMap(name=request.form.get('name'),
                               width=map_data['width'],
                               height=map_data['height'],
                               grid=json.dumps(map_data['grid']))
            if not map_item.name: map_item.name = '無標題'
            map_item.save()
            return redirect(url_for('map.list'))
    #從SDB 中取得map
    else:
        if mid:
            map_item = GameMap.get_by_id('map_'+str(mid))
        else:
            map_item = {
                    'width': request.args.get('w', 10, type=int),
                    'height': request.args.get('h', 10, type=int),
                    }
        return render_template('map_editor.html', map=map_item)
