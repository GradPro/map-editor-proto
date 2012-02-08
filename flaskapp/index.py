# -*- coding: UTF-8 -*-
import json
from flask import render_template, request, redirect, url_for
from main import app, sdb_con

dom = sdb_con.get_domain('game-maps')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/maps/')
def map_list():
    maps = dom.select(query="select mid, name, width, height from `game-maps`")
    return render_template('map_list.html', maps=maps)

@app.route('/maps/add/', methods=['GET', 'POST'])
def map_add():
    if request.method == 'POST':
        map_data = json.loads(request.form.get('map'))
        
        domain_meta = sdb_con.domain_metadata(dom)
        mid = domain_meta.item_count+1
        PK = 'map_' + str(mid)
        grid_json = json.dumps(map_data['grid'])
        grid_part = 1 if len(grid_json) < 1000 else (len(grid_json)//1000)+1
        attrs = {
                 'mid': mid,
                 'name': request.form.get('name', '無標題'),
                 'width': map_data['width'],
                 'height': map_data['height'],
                 'grid_part': grid_part,
                 }
        for part in xrange(grid_part):
            attrs['grid_'+ str(part+1)] = grid_json[part*1000:(part+1)*1000]
        dom.put_attributes(item_name=PK, attributes=attrs, replace=False)
        return redirect(url_for('map_list'))
    else:
        args = {
                'width': request.args.get('w', 10, type=int),
                'height': request.args.get('h', 10, type=int)
                }
        return render_template('map_editor.html', args=args)
