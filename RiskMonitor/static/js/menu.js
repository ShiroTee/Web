// $(document).ready(function () {
//     function getParentMenu() {
//         $.ajax({
//             type: 'GET',
//             dataType: 'json',
//             url: '/risk/menu/menus',
//             success: function (data) {
//                 var m = "";
//                 if (data.size > 0) {
//                     for (j = 0; j < data.size; j++) {
//                         if (data.data[j].parent_id == 0) {
//                             m = m + "<li roletype='2' id='" + data.data[j].menu_id + "' class='dropDown dropDown_hover'>" +
//                                     "<a class='dropDown_A' href='" + data.data[j].url + "'>" + data.data[j].menu_name + "<i class='fa fa-user' >" + '' + "</i></a></li>";
//                         }
//                     }
//                 }
//                 $('#ulmenu').html(m);
//                 $("#ulmenu li").bind('mouseover', function (e) {
//                      getSonMenu(this, e)
//                 });
//             }
//         });
//     }
//     getParentMenu();
//
//
//     function getSonMenu(event) {
//         var parentId = $(event).attr("id");
//         var roletype = $(event).attr("roletype");
//         if (roletype == "2")
//             $(event).addClass("hover open");
//         if (roletype == "1")
//             $(event).addClass("open");
//         if ($(event).find("li").length > 0 || roletype == "0") return;
//         $.ajax({
//             type: "get",
//             dataType: "json",
//             url: "/common/getSonMenu?parentId=" + parentId,
//             success: function (result) {
//                 var parentId = $(event).attr("id");
//                 $('#' + parentId).html($('#' + parentId + ' >a'))
//                 // $('#'+parentId).html("");
//                 var a = "<ul class='dropDown-menu menu radius box-shadow'>";
//                 var b = "</ul>";
//                 var c = "";
//                 $.each(result, function (i) {
//                     if(result[i].isnewblank == 1 && result[i].ishas_son == 1)
//                         {
//                             c = c + "<li roletype='" + result[i].ishas_son + "' id=" + result[i].node_id + "><a href='" + result[i].node_url + "' target='_blank'>" + result[i].node_showname + "<i class='arrow Hui-iconfont'></i></a></li>";
//                         }
//                     if(result[i].isnewblank == 1 && result[i].ishas_son == 0){
//                             c = c + "<li roletype='" + result[i].ishas_son + "' id=" + result[i].node_id + "><a href='" + result[i].node_url + "' target='_blank'>" + result[i].node_showname + "</a></li>";
//                     }
//                     if(result[i].isnewblank == 0 && result[i].ishas_son == 1){
//                             c = c + "<li roletype='" + result[i].ishas_son + "' id=" + result[i].node_id + "><a href='" + result[i].node_url + "'>" + result[i].node_showname + "<i class='arrow Hui-iconfont'></i></a></li>";
//                     }
//                     if(result[i].isnewblank == 0 && result[i].ishas_son == 0){
//                             c = c + "<li roletype='" + result[i].ishas_son + "' id=" + result[i].node_id + "><a href='" + result[i].node_url + "'>" + result[i].node_showname + "</a></li>";
//                     }
//                 });
//                 $('#' + parentId).append(a + c + b);
//                 $("#ulmenu li").unbind('mouseover');
//                 $("#ulmenu li").bind('mouseover', function (e) {
//                     getSonMenu(this, e)
//                 });
//             }, error: function (result) {
//                 alert(result.responseText);
//             }
//         });
//     }
//
// });


$(document).ready(function () {
    function initPage() {
        $.ajax({
            cache: true,
            type: 'GET',
            url: '/risk/menu/menus',  //调用自己本地写的接口，如果穿参数了,在getMenuInfo?+参数
            dataType: 'json',    //传入的数据类型是：json
            success: function (data) {     //这的data是接口查出来返回的数据
                var html = "";
                //定义一个空数据，从数据库动态获取的话，一个数组是没有办法取出子菜单信息的，用两个数组进行遍历
                var array = [];
                var ul = "";
                //我的菜单最顶层数据库给的是null，这里用null进行判断，若父菜单等于null的时候，则这个父菜单的子菜单就是一级目录，就是这里的子菜单已经是最顶级的了，变成了父菜单
                for (var i = 0; i < data.size; i++) {
                    if (data.data[i].parent_id == 0) {
                        //定义一个menuPid，将子菜单的值赋值给menuPid，这里menuPid是真正的父菜单
                        var menuPid = data.data[i].menu_id;

                        //这里的html不是页面，单纯的定义一个字段，里面遍历了拼接的li标签，这里面写的就是拼接的过程
                        html += '<li><a href="#" class="parentMenu" id="' + data.data[i].menu_id + '"><span><i class="' + data.data[i].url + '"></i>' + data.data[i].menu_name + '</span></a></li>';

                        //因为要显示出前面跳出来图片的样式，所以在这便利了子菜单的<div></div>标签
                        ul += '<div class="nav-slide-o"><ul id="pid' + data.data[i].menu_id + '"></ul></div>';
                        //将父菜单赋值给这个空数组array，这个array现在里面的值全部都是父菜单信息
                        array.push(menuPid);
                    }
                }

                //因为我前台定义的是ul的id，所以把遍历出来的父菜单信息塞给前台的ul标签，到时候就需要写前台里面的li了，直接是上面拼接出来的一个 < li > < /li>,这里就是从数据库动态取出来的父菜单信息
                $("#pmenuid").append(html);

                //这是将遍历出来的子菜单信息塞到前台页面的div中
                $("#menuInfo").append(ul);
                var url = "";

                //子菜单跟父菜单是一一对应的关系所以这里将通过父菜单取出子菜单，并且将子菜单放入到父菜单的节点下
                for (var i = 0; i < data.size; i++) {
                    for (var j = 0; j < array.length; j++) {      //array.length是父菜单的长度
                        if (data.data[i].parent_id == array[j]) {

                            //url是我拼接出来的子菜单信息，并且将子菜单放入到父菜单的节点下
                            url += $("#pid" + array[j] + "").append(
                                '<li><a class="childMenu"  onclick="changeCont(&quot;' + data.data[i].url + '&quot;)"><span>' + data.data[i].menu_name + '</span></a></li>'
                            );
                        }
                    }
                }
            }
        });
    }
    initPage()
});











