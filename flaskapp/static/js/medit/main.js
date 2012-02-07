//==================== 全域物件 ====================
var game = {};

//==================== 工具函式 ====================
//此內建function為實驗性功能，所以要做測試取得，依序為標準名稱、Firefox、Chrome/Safari、IE(v10)、和setTimeout(60fps)相容版
var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||  
                        window.webkitRequestAnimationFrame || window.msRequestAnimationFrame ||
                        function(fn){ setTimeout(fn, 1000/60); };
//產生一個新的<canvas>物件
game.Cvs = function(){ return document.createElement('canvas'); }
//回傳canvas的2D繪圖API介面
game.Ctx = function(canvas){ return canvas.getContext('2d'); }

//==================== DOM ready ====================
$(function(){
//從全域物件匯入
var Cvs = game.Cvs, Ctx = game.Ctx,
    chunkSize = game.chunkSize, map = game.map;
    ui = game.ui;

//==================== DOM ====================
//地圖圖層
var $mlayer = $('canvas#map'), mlayer = $mlayer[0], mlayer_ctx = Ctx(mlayer);
//介面圖層，光棒及反白等等
var $uilayer = $('canvas#ui'), uilayer = $uilayer[0], uilayer_ctx = Ctx(uilayer);
//面板
var $pane = $('div.pane');
//debug面板
var $dbg = $('div#debug>div.content'), $dbgp = $('div#debug');
//地形清單面板
var $cList = $('div#chunkList>div.content'), $cListP = $('div#chunkList');
//掛到全域物件上
game.$mlayer = $mlayer; game.mlayer = mlayer; game.mlayer_ctx = mlayer_ctx;
game.$uilayer = $uilayer; game.uilayer = uilayer; game.uilayer_ctx = uilayer_ctx;
game.$pane = $pane;
game.$dbg = $dbg; game.$dbgp = $dbgp;
game.$cList = $cList; game.$cListP = $cListP;

//==================== layout ====================
//依照地圖大小計算canvas大小
mlayer.width = (map.width+2) * chunkSize;
mlayer.height = (map.height+2) * chunkSize;
//全畫面
function uiResize(){
    uilayer.width = $(window).width();
    uilayer.height = $(window).height();
}
uiResize(); //初始全畫面
$(window).resize(uiResize); //如果使用者調整視窗大小，跟著調整畫面
//動態設定位置
$mlayer.offset({left: ui.left, top: ui.top});

//檔案動作
$('#btn_cancel').click(function(){
	if (confirm('確定放棄編輯？')){
		history.back();
	}
});

});
