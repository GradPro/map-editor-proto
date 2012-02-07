//==================== DOM ready ====================
$(function(){
//從全域物件匯入
var $pane = game.$pane, uilayer = game.uilayer;

$pane.each(function(i){
    $(this).offset({left: 200 + i * 200,
                    top: 100 + i * 100});
});

//面板可拖曳
$pane.children('div.caption').mouseover(function(){
    var $mecap = $(this);
    var $mepane = $mecap.parents('div.pane');
    var $mecontent = $mecap.next('div.content');
    if (!$mecap.next('canvas.cap_mask').length) {
        $mecap.after('<canvas class="cap_mask">');
        $mecap.next('canvas.cap_mask').attr('title', '拖曳移動，雙點收合與展開');
    }
    var $memask = $mecap.next('canvas.cap_mask'), memask = $memask[0];
    $memask.offset($mecap.offset());
    memask.width = $mecap.width();
    memask.height = $mecap.height();

    $memask.mousedown(function(evt){
        var pos = $mepane.offset();
        var off = { left: evt.clientX-pos.left, top: evt.clientY-pos.top };
        function drag(e){
            $mepane.offset({ left: e.clientX-off.left, top: e.clientY-off.top });
            $memask.offset($mecap.offset());
        }
        function stopDrag(e){ $memask.unbind('mousemove', drag).unbind('mouseleave', drag); }
        $memask.mousemove(drag).mouseleave(drag).mouseup(stopDrag);
    }).dblclick(function(){
        $mecontent.slideToggle(function(){
            memask.width = $mecap.width();
            memask.height = $mecap.height();
        });
    });
});

});