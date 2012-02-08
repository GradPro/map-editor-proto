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
    maps = dom.select(query="select mid, name, width, height from `game-maps`",
                      consistent_read=True)
    return render_template('map_list.html', maps=maps)

def map_editor(mid=None):
    #將map存於SDB
    if request.method == 'POST':
        map_data = json.loads(request.form.get('map'))
        if mid:
            map_item = dom.get_item('map_'+str(mid), consistent_read=True)
            map_item['name'] = request.form.get('name', 'Untitled')
            grid_json = json.dumps(map_data['grid'])
            for part in xrange(int(map_item['grid_part'], 10)):
                map_item['grid_'+ str(part+1)] = grid_json[part*1000:(part+1)*1000]
            map_item.save(replace=True)
            return redirect(url_for('map_list'))
        else:
            #取得在SDB 上item 的數量
            domain_meta = sdb_con.domain_metadata(dom)
            mid = domain_meta.item_count+1
            PK = 'map_' + str(mid)
            grid_json = json.dumps(map_data['grid'])
            #計算grid所需的拆分後的grid_part數目
            grid_part = 1 if len(grid_json) < 1000 else (len(grid_json)//1000)+1
            attrs = {
                     'mid': mid,
                     'name': request.form.get('name', 'Untitled'),
                     'width': map_data['width'],
                     'height': map_data['height'],
                     'grid_part': grid_part,
                     }
            #將grid 拆成 grid_1, grid_2,...
            for part in xrange(grid_part):
                attrs['grid_'+ str(part+1)] = grid_json[part*1000:(part+1)*1000]
            dom.put_attributes(item_name=PK, attributes=attrs, replace=False)
            return redirect(url_for('map_list'))
    #從SDB 中取得map
    else:
        if mid:
            map_item = dom.get_item('map_'+str(mid), consistent_read=True)
            grid_json = ''
            for part in xrange(int(map_item['grid_part'], 10)):
                grid_json += map_item['grid_'+str(part+1)]
            args = {
                    'mid': map_item['mid'],
                    'width': map_item['width'],
                    'height': map_item['height'],
                    'name': map_item['name'],
                    }
            return render_template('map_editor.html', args=args, grid=grid_json)
        else:
            args = {
                    'width': request.args.get('w', 10, type=int),
                    'height': request.args.get('h', 10, type=int),
                    'name': 'Untitled'
                    }
            return render_template('map_editor.html', args=args)

app.add_url_rule('/maps/edit/<int:mid>', 'map_edit', map_editor, methods=['GET', 'POST'])
app.add_url_rule('/maps/add/', 'map_add', map_editor, methods=['GET', 'POST'])
