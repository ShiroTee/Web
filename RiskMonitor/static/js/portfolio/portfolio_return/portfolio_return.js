// js 用到的框架: layui, echarts
// layui 文档地址: https://www.layui.com/doc/
// echarts 文档地址: https://echarts.apache.org/zh/option.html#title
// 注意: 需要在contenthtml配置layui的css, js文件, echarts的css, js文件, xm-select的js文件
"use strict";

// 起止日期框
layui.use(['okLayer','laydate'], function(){

      var laydate = layui.laydate;
      var okLayer = layui.okLayer;

      //执行一个laydate实例
      laydate.render({
        elem: '#start_date1', //指定元素
        done: function(value,date){
            // 直接获得start值
            var start = value;
            // ajax获得end值
            var end = $('#end_date1').val();
            if (start && end){
                if (start > end){
                    var start_reset = document.getElementById("start_date1")
                    var end_reset = document.getElementById("end_date1")
                    start_reset.value=''
                    end_reset.value=''
                    okLayer.msg.redCross("起止日期错误", function () {
                        });
                    }
                }
            }
      });

      laydate.render({
        elem: '#start_date2', //指定元素
        // 监听值
        done: function(value,date){

        // 直接获得start值
        var start = value;
        // ajax获得end值
        var end = $('#end_date2').val();
        // 通过xmSelect获得code值
        var code = xmSelect.get('#code_lst2', true);
        code = code.getValue('name')[0];

        // start,end,code都有值才执行
        if (start && end && code){

            if (start < end){
                                    $.ajax({
                                     type:'get',
                                     url:'./portfolioReturn/get_index',
                                     async:false,
                                     cache:false,
                                     data:{
                                       'code': code,
                                       'end': end
                                      },
                                     dataType:'json',
                                     success:function(response){

                                          var res = response.data;
                                          var index_lst1 = xmSelect.get('#index_lst1', true);
                                           // 返回基准代码数组
                                          index_lst1.update({
                                                data: res,
                                                autoRow: true,
                                            });
                                           }
                                     });}
            else{
                var start_reset = document.getElementById("start_date2")
                var end_reset = document.getElementById("end_date2")
                var index_lst1 = xmSelect.get('#index_lst1', true);
                index_lst1.update({
                                                    data: [],
                                                    autoRow: true,
                                                });
                start_reset.value=''
                end_reset.value=''

                okLayer.msg.redCross("起止日期错误", function () {
                        });
                }

        }
                // 如果不满足 基准下拉框设为空
        else{
            var index_lst1 = xmSelect.get('#index_lst1', true);
            index_lst1.update({
                                                data: [],
                                                autoRow: true,
                                            });}

        }
      });

      laydate.render({
        elem: '#end_date1', //指定元素
        done: function(value,date){
            var end = value;
            // ajax获得start值
            var start = $('#start_date1').val();
            if (start && end){
                if (start > end){
                    var start_reset = document.getElementById("start_date1")
                    var end_reset = document.getElementById("end_date1")
                    start_reset.value=''
                    end_reset.value=''
                    okLayer.msg.redCross("起止日期错误", function () {
                        });
                    }
                }
            }

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
            if (start < end){
                                $.ajax({
                                     type:'get',
                                     url:'./portfolioReturn/get_index',
                                     async:false,
                                     cache:false,
                                     data:{
                                       'code': code,
                                       'end': end
                                      },
                                     dataType:'json',
                                     success:function(response){

                                          var res = response.data;
                                          var index_lst1 = xmSelect.get('#index_lst1', true);
                                           // 返回基准代码数组
                                          index_lst1.update({
                                                data: res,
                                                autoRow: true,
                                            });
                                           }
                                     });
                              }
             else{
                var start_reset = document.getElementById("start_date2")
                var end_reset = document.getElementById("end_date2")
                var index_lst1 = xmSelect.get('#index_lst1', true);
                index_lst1.update({
                               data: [],
                               autoRow: true,
                    });
                start_reset.value=''
                end_reset.value=''
                okLayer.msg.redCross("起止日期错误", function () {
                        });
                }
        }
                // 如果不满足 基准下拉框设为空
        else{
            var index_lst1 = xmSelect.get('#index_lst1', true);
            index_lst1.update({
                           data: [],
                           autoRow: true,
                });}

        }
      });
    });


// 组合业绩表
layui.use('form', function(){
// 声明表单
var form = layui.form;

// 声明图
var myChart1 = echarts.init(document.getElementById('portfolio_graph1'));
    // 显示标题，图例和空的坐标轴等图变量
    var option = {
        title: {
            text: ''
        },
        // 提示框
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                    type: 'cross'
                },
            position: function (pt) {
                return [pt[0], '10%'];
            },
            // 提示框格式转换为百分号
            formatter: function(params){
                var result = params[0].name + '<br>';
                params.forEach(function(item) {
                  if (item.value) {
                    var item_value = item.value[1]*100
                    result += item.marker + " " + item.seriesName + " : " + item_value.toFixed(2) + "%</br>";
                  } else {
                    result += item.marker + " " + item.seriesName + " :  - </br>";
                  }
                });

                return result;
                }
        },
        // 图例
        legend: {
                top: 10,
                left: 'center',

                data: []
            },
        xAxis: {
            data: []
        },
        // Y轴坐标转换为百分号
        yAxis: {
        axisLabel:{
                        formatter:function (value, index) {
        return (value*100).toFixed(0)+'%';
                                               }
                   }
        },
        // 横坐标缩放
        dataZoom: [
            {   // 这个dataZoom组件，默认控制x轴。
                type: 'slider', // 这个 dataZoom 组件是 slider 型 dataZoom 组件
                start: 0,      // 左边在 0% 的位置。
                end: 100         // 右边在 100% 的位置。
            }
        ],
        // 每个系列通过 type 决定自己的图表类型
        series: [
        ]
    };

    // 应用option
    myChart1.setOption(option);



  // 监听提交 通过button里的lay-filter='formDemo'监听
  form.on('submit(formDemo1)', function(res){

    // 通过表单对象res.field得到起止时间
    var start = res.field.start;
    var end = res.field.end;
    var code;
    var code_lst;

    // 得到多选框中的字符串数组
	code = xmSelect.get('#code_lst1', true);
    code_lst = code.getValue('name');


    $.ajax({
        type:'get',
         // 通过url调用视图函数
         url:'./portfolioReturn/get_start_end',
         // async:true 异步请求
         async:true,
         cache:false,
         // 向后台传回data里的参数
         data:{
         'start': start,
         'end': end,
         // 注意: 如果传回数组, 需要json化
         'code_lst': JSON.stringify(code_lst)
         },
         dataType:'json',
         traditional: true,
         // 返回成功, 执行函数
         success:function(res){
              var series = [];
              // 将返回的值push进series数组中
              for (var i = 0; i < code_lst.length; i++) {
                      series.push({
                                type:'line',
                                // series的name要和legend.data保持一致
                                name: code_lst[i],
                                data: res[code_lst[i]]
                          });
                    };
              option.xAxis.data = res.xlab;
              option.series = series;
              option.legend.data = code_lst;
              // 设置为true可处理数据遗留问题
              myChart1.setOption(option, true);

               }
         });

    // 监听缩放
    myChart1.on('datazoom', function (params) {
      // 得到缩放的起止日期
      var startX = myChart1.getOption().dataZoom[0].endValue;
      var endX = myChart1.getOption().dataZoom[0].startValue;
      var endTime = option.xAxis.data[startX];
      var startTime = option.xAxis.data[endX];

      code = xmSelect.get('#code_lst1', true);
      code_lst = code.getValue('name');

      $.ajax({
         type:'get',
         // 通过url调用视图函数
         url:'./portfolioReturn/get_start_end',
         // async:true 异步请求
         async:true,
         cache:false,
         data:{
         'start': startTime,
         'end': endTime,
         // 注意: 如果传回数组, 需要json化
         'code_lst': JSON.stringify(code_lst)
         },
         dataType:'json',
         traditional: true,
         // 返回成功, 执行函数
         success:function(res){
              var series = []
              // 此时只需修改series数组里的data
              for (var i = 0; i < code_lst.length; i++) {

                      series.push({
                                type:'line',
                                name: code_lst[i],
                                data: res[code_lst[i]]
                          });
                    };
                // 应用option 这里myChart.setOption({})修改里面的series
                myChart1.setOption({
                series: series
          });
             }
         });

        });
    // 提交表单后不刷新
    return false;
  });


});




// 组合基准对比表
layui.use('form', function(){
// 声明表单
var form = layui.form;

// 声明图
var myChart2 = echarts.init(document.getElementById('portfolio_graph2'));
    // 显示标题，图例和空的坐标轴等图变量
    var option = {
        title: {
            text: ''
        },
        // 提示框
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                    type: 'cross'
                },
            position: function (pt) {
                return [pt[0], '10%'];
            },
            // 提示框格式转换为百分号
            formatter: function(params){
                var result = params[0].name + '<br>';
                params.forEach(function(item) {
                  if (item.value) {
                    var item_value = item.value[1]*100
                    result += item.marker + " " + item.seriesName + " : " + item_value.toFixed(2) + "%</br>";
                  } else {
                    result += item.marker + " " + item.seriesName + " :  - </br>";
                  }
                });

                return result;
                }
        },
        // 图例
        legend: {
                top: 10,
                left: 'center',

                data: []
            },
        xAxis: {
            data: []
        },
        // Y轴坐标转换为百分号
        yAxis: {
        axisLabel:{
                        formatter:function (value, index) {
        return (value*100).toFixed(0)+'%';
                                               }
                   }
        },
        // 横坐标缩放
        dataZoom: [
            {   // 这个dataZoom组件，默认控制x轴。
                type: 'slider', // 这个 dataZoom 组件是 slider 型 dataZoom 组件
                start: 0,      // 左边在 0% 的位置。
                end: 100         // 右边在 100% 的位置。
            }
        ],
        // 每个系列通过 type 决定自己的图表类型
        series: [
        ]
    };

    // 应用option
    myChart2.setOption(option);

    // 监听提交 通过button里的lay-filter='formDemo2'监听
  form.on('submit(formDemo2)', function(res){
    // 通过表单对象res.field得到起止时间
    var start = res.field.start;
    var end = res.field.end;
    var code = xmSelect.get('#code_lst2', true);
    var code_lst = code.getValue('name');
    var index = xmSelect.get('#index_lst1', true);
    var index_lst = index.getValue('name');


    // 得到多选框中的字符串数组


    $.ajax({
        type:'get',
         // 通过url调用视图函数
         url:'./portfolioReturn/get_start_end_index',
         // async:true 异步请求
         async:true,
         cache:false,
         // 向后台传回data里的参数
         data:{
         'start': start,
         'end': end,
         'code': JSON.stringify(code_lst),
         // 注意: 如果传回数组, 需要json化
         'index_lst': JSON.stringify(index_lst)
         },
         dataType:'json',
         traditional: true,
         // 返回成功, 执行函数
         success:function(res){
              var series = [];
              series.push({
                                type:'line',
                                // series的name要和legend.data保持一致
                                name: code_lst[0],
                                data: res[code_lst[0]]
              });

              for (var i = 0; i < index_lst.length; i++) {
                      series.push({
                                type:'line',
                                // series的name要和legend.data保持一致
                                name: index_lst[i],
                                data: res[index_lst[i]]
                          });
                      code_lst.push(index_lst[i])

                    };

              option.xAxis.data = res.xlab;
              option.series = series;
              option.legend.data = code_lst;
              // 设置为true可处理数据遗留问题

              myChart2.setOption(option, true);

               }
         });



    // 监听缩放
    myChart2.on('datazoom', function (params) {
      // 得到缩放的起止日期
      var startX = myChart2.getOption().dataZoom[0].endValue;
      var endX = myChart2.getOption().dataZoom[0].startValue;
      var endTime = option.xAxis.data[startX];
      var startTime = option.xAxis.data[endX];

      code = xmSelect.get('#code_lst2', true);
      code_lst = code.getValue('name');
      index = xmSelect.get('#index_lst1', true);
      index_lst = index.getValue('name');



      $.ajax({
         type:'get',
         // 通过url调用视图函数
         url:'./portfolioReturn/get_start_end_index',
         // async:true 异步请求
         async:false,
         cache:false,
         data:{
         'start': startTime,
         'end': endTime,
         'code': JSON.stringify(code_lst),
         // 注意: 如果传回数组, 需要json化
         'index_lst': JSON.stringify(index_lst)
         },
         dataType:'json',
         traditional: true,
         // 返回成功, 执行函数
         success:function(res){
              var series = [];

              series.push({
                                type:'line',
                                // series的name要和legend.data保持一致
                                name: code_lst[0],
                                data: res[code_lst[0]]
              });

              for (var i = 0; i < index_lst.length; i++) {
                      series.push({
                                type:'line',
                                // series的name要和legend.data保持一致
                                name: index_lst[i],
                                data: res[index_lst[i]]
                          });

                    };
               myChart2.setOption({
                series: series
                     });


             }
         });

        });
    // 提交表单后不刷新
    return false;
  });



});























        form.on('submit(edit)', function (data) {
                    var checkData = tree.getChecked('roletree');
                    $.ajax({
                         type:'POST',
                         url:'./update',
                         async:true,
                         cache:false,
                         data:{
                         'role_id': initData.l_role_id,
                         'checkData': JSON.stringify(checkData)
                         },
                         traditional: true,
                         dataType:'json',
                         success:function(res){
                             }
                         });
                    layer.msg("编辑成功！", {icon: 6, time: 1000, anim: 4}, function () {
                        parent.layer.close(parent.layer.getFrameIndex(window.name));
                    });
                    return false;
                });






















