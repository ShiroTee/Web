$(function(){
	genVerCode();//初始化生成随机数
});

//生成随机数
function genVerCode(len){
    len = len || 4;
    var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';//默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1
    var maxPos = $chars.length;
    var genCode = '';
    for (i = 0; i < len; i++) {
        genCode += $chars.charAt(Math.floor(Math.random() * maxPos));
    }
    $(".genVerCode").html(genCode);
}