//介面相關
game.ui = {
//地圖圖層捲動偏移值
    left: 0,
    top: 0,
//捲動方向向量
    scroll: [0,0]
};

//==================== DOM ready ====================
$(function(){
//從全域物件匯入
var ui = game.ui, map = game.map, chunkSize = game.chunkSize, chunkList = game.chunkList,
    $uilayer = game.$uilayer, uilayer = game.uilayer, uilayer_ctx = game.uilayer_ctx,
    $mlayer = game.$mlayer, mlayer = game.mlayer, mlayer_ctx = game.mlayer_ctx,
    $dbg = game.$dbg;
//UI圖層更新
function uiUpdate(evt){
    if (evt && evt.type) { ui.x = evt.clientX, ui.y = evt.clientY; }
    ui.mx = ui.x - ui.left;
    ui.my = ui.y - ui.top;

    ui.scroll = [0,0];
    if (ui.x<chunkSize*2 && ui.left < 0) {
        ui.scroll[0] = -1;
    }
    else if (ui.x>uilayer.width-chunkSize*2 && -ui.left<mlayer.width-uilayer.width) {
        ui.scroll[0] = 1;
    }
    if (ui.y<chunkSize*2 && ui.top < 0) {
        ui.scroll[1] = -1;
    }
    else if (ui.y>uilayer.height-chunkSize*2 && -ui.top<mlayer.height-uilayer.height) {
        ui.scroll[1] = 1;
    }

    var cursor = '';
    if (ui.scroll[0] == 0 && ui.scroll[1] == 0) { cursor = 'auto'; }
    else {
        if (ui.scroll[1]<0) { cursor += 'n'; }
        else if (ui.scroll[1]>0) { cursor += 's'; }
        if (ui.scroll[0]<0) { cursor += 'w'; }
        else if (ui.scroll[0]>0) { cursor += 'e'; }
        cursor += '-resize';
        $mlayer.offset({left: parseInt(ui.left -= ui.scroll[0]),
                        top: parseInt(ui.top -= ui.scroll[1])});
        setTimeout(uiUpdate, 100);
    }
    $uilayer.css('cursor', cursor);

    if (ui.mx > chunkSize + map.width*chunkSize ||
      ui.my > chunkSize + map.height*chunkSize ||
      ui.mx < chunkSize || ui.my < chunkSize) {
      map.hover.x = map.hover.y = -1;
      } else {
          map.hover.x = parseInt((ui.mx-chunkSize-1)/chunkSize, 10);
          map.hover.y = parseInt((ui.my-chunkSize-1)/chunkSize, 10);
      }
      $dbg.html('游標位置: ('+ui.x+','+ui.y+')<br>'+
                '區塊位置: ('+map.hover.x+','+map.hover.y+')<br>'+
                '選擇地形: '+map.placeChunk+'<br>'+
                '目標地形: '+
                ((map.hover.x >= 0 && map.hover.y >= 0)? map.grid[map.hover.x][map.hover.y] :-1));
}

function uiClick(evt){
  if(map.hover.x >= 0 && map.hover.y >= 0) {
    mlayer_ctx.drawImage(chunkList[map.placeChunk].cvs,
                         chunkSize + map.hover.x*chunkSize,
                         chunkSize + map.hover.y*chunkSize);
    map.grid[map.hover.x][map.hover.y] = map.placeChunk;
  }
}

$uilayer.mousemove(uiUpdate).click(uiClick);

//劃出滑鼠所在區塊的標示色塊
function drawHover(t){
    //清空畫面
    uilayer_ctx.clearRect(0,0,uilayer.width,uilayer.height);
    if (map.hover.x >= 0 && map.hover.y >= 0){
        if (chunkList[map.placeChunk].cvs) {
            uilayer_ctx.drawImage(chunkList[map.placeChunk].cvs,
                                  chunkSize + map.hover.x*chunkSize + ui.left,
                                  chunkSize + map.hover.y*chunkSize + ui.top);
        }
    }
    if (!(ui.scroll[0] == 0 && ui.scroll[1] == 0)) {
        var v = (uilayer.width-chunkSize*2) /2, h = (uilayer.height-chunkSize*2) /2;
        uilayer_ctx.fillStyle = 'rgba(0,0,0,0.1)';
        if (ui.scroll[0] != 0) {
            uilayer_ctx.fillRect(v+v*ui.scroll[0], 0, chunkSize*2, uilayer.height);
        }
        if (ui.scroll[1] != 0) {
            uilayer_ctx.fillRect(0, h+h*ui.scroll[1], uilayer.width, chunkSize*2);
        }
    }
    requestAnimationFrame(drawHover);
}

requestAnimationFrame(drawHover);
});