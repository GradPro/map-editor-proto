function render_template(tpl, ctx){
// 陽春的js樣板顯示函式
    // 尋覽一次所有要顯示的變數
    $.each(ctx, function(k, v){
        // 對應的顯示位置，如果出現不只一次，代表全部的位置
        re = RegExp('{{'+ k +'}}', 'g')
        // 找出位置代換為變數值
        tpl = tpl.replace(re, v);
    })
    return tpl;
}

$(function(){
    url = '/api/maps'; // REST api 存取點
    $target = $('#map_list'); // 資料插入位置
    // 樣板
    tpl = '<tr>' +
          '<td>{{id}}</td>' +
          '<td>{{mid}}</td>' +
          '<td>{{name}}</td>' +
          '<td>{{width}}</td>' +
          '<td>{{height}}</td>' +
          '<td><a class="btn btn-success btn-small" href="{{edit}}">' +
          '<i class="icon-play icon-white"></i> 進入</a></td>' +
          '</tr>';
    // 從 REST api 取回 JSON 格式的資料
    $.getJSON(url, function(data){
        list = data.maps;
        // 清空
        $target.empty();
        // 插入所有資料
        $.each(list, function(i, v){
            prop = v.properties;
            edit_url = edit_map_url.replace('0', prop.mid);
            ctx = {id: v.id, mid: prop.mid, name: prop.name,
                   width: prop.width, height: prop.height, edit: edit_url};
            $target.append(render_template(tpl, ctx));
        });
    });
});
