// js 用到的框架: layui, echarts
// layui 文档地址: https://www.layui.com/doc/
// echarts 文档地址: https://echarts.apache.org/zh/option.html#title
// 注意: 需要在base.html配置layui的css, js文件, echarts的css, js文件, xm-select的js文件


layui.use('form', function(){
// 声明表单
var form = layui.form;

// 声明图
var myChart = echarts.init(document.getElementById('portfolio_graph2'));
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
                start: 0,      // 左边在 10% 的位置。
                end: 100         // 右边在 60% 的位置。
            }
        ],
        // 每个系列通过 type 决定自己的图表类型
        series: [
        ]
    };

    // 应用option
    myChart.setOption(option);

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
         url:'/correct/graph1/get_start_end_index',
         // async:true 异步请求 此时不修改全局变量
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
         // 如果传回数组, 需要加traditional: true
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

              for (i = 0; i < index_lst.length; i++) {
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

              myChart.setOption(option, true);

               }
         });



    // 监听缩放
    myChart.on('datazoom', function (params) {
      // 得到缩放的起止日期
      var startX = myChart.getOption().dataZoom[0].endValue;
      var endX = myChart.getOption().dataZoom[0].startValue;
      var endTime = option.xAxis.data[startX];
      var startTime = option.xAxis.data[endX];

      code = xmSelect.get('#code_lst2', true);
      code_lst = code.getValue('name');
      index = xmSelect.get('#index_lst1', true);
      index_lst = index.getValue('name');

      console.log(startTime);
      console.log(endTime);

      $.ajax({
         type:'get',
         // 通过url调用视图函数
         url:'/correct/graph1/get_start_end_index',
         // async:true 异步请求 此时不修改全局变量
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
         // 如果传回数组, 需要加traditional: true
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

              for (i = 0; i < index_lst.length; i++) {
                      series.push({
                                type:'line',
                                // series的name要和legend.data保持一致
                                name: index_lst[i],
                                data: res[index_lst[i]]
                          });

                    };
               myChart.setOption({
                series: series
                     });


             }
         });

        });
    // 提交表单后不刷新
    return false;
  });



});