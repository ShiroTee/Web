layui.use('laydate', function(){

      var laydate = layui.laydate;

      //执行一个laydate实例
      laydate.render({
        elem: '#start_date1' //指定元素
      });

      laydate.render({
        elem: '#start_date2', //指定元素
        // 监听值
        done: function(value,date){

        // 直接获得start值
        var start = value;
        // ajax获得end值
        var end = $('#end_date2').val();
        // 通过xmSelect蝴蝶code值
        var code = xmSelect.get('#code_lst2', true);
        code = code.getValue('name')[0];
        // start,end,code都有值才执行
        if (start && end && code){
                                $.ajax({
                                     type:'get',
                                     url:'/correct/graph1/get_index',
                                     async:false,
                                     cache:false,
                                     data:{
                                       'code': code,
                                       'end': end
                                      },
                                     dataType:'json',
                                     success:function(response){
                                          var res = response.data;
                                           // 返回基准代码数组
                                          index_lst1.update({
                                                data: res,
                                                autoRow: true,
                                            });
                                           }
                                     });
                              }
                // 如果不满足 基准下拉框设为空
                else{index_lst1.update({
                                                data: [],
                                                autoRow: true,
                                            });}

        }
      });

      laydate.render({
        elem: '#end_date1' //指定元素
      });

      laydate.render({
        elem: '#end_date2', //指定元素
        // 监听值
        done: function(value,date){
        // ajax获得start值
        var start = $('#start_date2').val();
        // 直接获得end值
        var end = value;
        // 通过xmSelect获得code
        var code = xmSelect.get('#code_lst2', true);
        code = code.getValue('name')[0];

        if (start && end && code){
                                $.ajax({
                                     type:'get',
                                     url:'/correct/graph1/get_index',
                                     async:false,
                                     cache:false,
                                     data:{
                                       'code': code,
                                       'end': end
                                      },
                                     dataType:'json',
                                     success:function(response){
                                          var res = response.data;
                                           // 返回基准代码数组
                                          index_lst1.update({
                                                data: res,
                                                autoRow: true,
                                            });
                                           }
                                     });
                              }
                // 如果不满足 基准下拉框设为空
                else{index_lst1.update({
                                                data: [],
                                                autoRow: true,
                                            });}

        }
      });
    });





