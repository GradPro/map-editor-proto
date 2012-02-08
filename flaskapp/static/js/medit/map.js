game.map.grid = [];
game.map.placeChunk = 1;

//滑鼠目前位置所在的區塊，-1表示不在任何一個上面
game.map.hover = {x: -1, y: -1};
//每個區塊的尺寸，單位px
game.chunkSize = 30;

//==================== DOM ready ====================
$(function(){
//從全域物件匯入
var map = game.map, chunkSize = game.chunkSize, mlayer_ctx = game.mlayer_ctx;
//載入地形圖塊
(function(){
    //從全域物件匯入
    var chunkList = game.chunkList, $cList = game.$cList,
        Cvs = game.Cvs, Ctx = game.Ctx;
    var img = new Image();
    img.src = chunkList.src;
    img.onload = function(){
        for(var x = 1; x <= chunkList.len; x++){
            var cvs = Cvs(), ctx = Ctx(cvs);
            cvs.width = cvs.height = chunkSize;
            ctx.drawImage(chunkList.img,
                          chunkList[x].x,chunkList[x].y,chunkSize,chunkSize,
                          0,0,chunkSize,chunkSize);
            chunkList[x].cvs = cvs;
            $cList.append('<img data-terrain="'+ x +'" title="地形編號 '+x+'" '+
                          'src="'+ chunkList[x].cvs.toDataURL() +'"><br>');
        }
        $cList.find('img').click(function(){ map.placeChunk = parseInt($(this).data('terrain')); });
    }
    chunkList.img = img;
})();

//畫區塊定位點，四個角個一點(1x1 px)
for (var x = 1; x <= map.width; x++)
    for (var y = 1; y <= map.height; y++){
        var left = chunkSize * x, top = chunkSize * y;
        mlayer_ctx.fillRect(left, top, 1, 1);
        mlayer_ctx.fillRect(left + chunkSize-1, top, 1, 1);
        mlayer_ctx.fillRect(left, top + chunkSize-1, 1, 1);
        mlayer_ctx.fillRect(left + chunkSize-1, top + chunkSize-1, 1, 1);
        mlayer_ctx.fillText(x-1, left, top+12);
        mlayer_ctx.fillText(y-1, left, top+26);
    }

});
