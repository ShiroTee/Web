// js �õ��Ŀ��: layui, echarts
// layui �ĵ���ַ: https://www.layui.com/doc/
// echarts �ĵ���ַ: https://echarts.apache.org/zh/option.html#title
// ע��: ��Ҫ��base.html����layui��css, js�ļ�, echarts��css, js�ļ�, xm-select��js�ļ�
"use strict";

// ��ֹ���ڿ�
layui.use(['okLayer','laydate'], function(){

      var laydate = layui.laydate;
      var okLayer = layui.okLayer;

      //ִ��һ��laydateʵ��
      laydate.render({
        elem: '#start_date1', //ָ��Ԫ��
        done: function(value,date){
            var start = value;
            // ajax���endֵ
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
        elem: '#start_date2', //ָ��Ԫ��
        // ����ֵ
        done: function(value,date){

        // ֱ�ӻ��startֵ
        var start = value;
        // ajax���endֵ
        var end = $('#end_date2').val();
        // ͨ��xmSelect����codeֵ
        var code = xmSelect.get('#code_lst2', true);
        code = code.getValue('name')[0];

        // start,end,code����ֵ��ִ��
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
                                           // ���ػ�׼��������
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
                // ��������� ��׼��������Ϊ��
        else{
            var index_lst1 = xmSelect.get('#index_lst1', true);
            index_lst1.update({
                                                data: [],
                                                autoRow: true,
                                            });}

        }
      });

      laydate.render({
        elem: '#end_date1', //ָ��Ԫ��,
        done: function(value,date){
            var end = value;
            // ajax���endֵ
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
        elem: '#end_date2', //ָ��Ԫ��
        // ����ֵ
        done: function(value,date){
        // ajax���startֵ
        var start = $('#start_date2').val();
        // ֱ�ӻ��endֵ
        var end = value;
        // ͨ��xmSelect���code
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
                                           // ���ػ�׼��������
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
                // ��������� ��׼��������Ϊ��
        else{
            var index_lst1 = xmSelect.get('#index_lst1', true);
            index_lst1.update({
                           data: [],
                           autoRow: true,
                });}

        }
      });
    });


// ���ҵ����
layui.use('form', function(){
// ������
var form = layui.form;

// ����ͼ
var myChart1 = echarts.init(document.getElementById('portfolio_graph1'));
    // ��ʾ���⣬ͼ���Ϳյ��������ͼ����
    var option = {
        title: {
            text: ''
        },
        // ��ʾ��
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                    type: 'cross'
                },
            position: function (pt) {
                return [pt[0], '10%'];
            },
            // ��ʾ���ʽת��Ϊ�ٷֺ�
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
        // ͼ��
        legend: {
                top: 10,
                left: 'center',

                data: []
            },
        xAxis: {
            data: []
        },
        // Y������ת��Ϊ�ٷֺ�
        yAxis: {
        axisLabel:{
                        formatter:function (value, index) {
        return (value*100).toFixed(0)+'%';
                                               }
                   }
        },
        // ����������
        dataZoom: [
            {   // ���dataZoom�����Ĭ�Ͽ���x�ᡣ
                type: 'slider', // ��� dataZoom ����� slider �� dataZoom ���
                start: 0,      // ����� 10% ��λ�á�
                end: 100         // �ұ��� 60% ��λ�á�
            }
        ],
        // ÿ��ϵ��ͨ�� type �����Լ���ͼ������
        series: [
        ]
    };

    // Ӧ��option
    myChart1.setOption(option);



  // �����ύ ͨ��button���lay-filter='formDemo'����
  form.on('submit(formDemo1)', function(res){

    // ͨ��������res.field�õ���ֹʱ��
    var start = res.field.start;
    var end = res.field.end;
    var code;
    var code_lst;

    // �õ���ѡ���е��ַ�������
	code = xmSelect.get('#code_lst1', true);
    code_lst = code.getValue('name');


    $.ajax({
        type:'get',
         // ͨ��url������ͼ����
         url:'./portfolioReturn/get_start_end',
         // async:true �첽���� ��ʱ���޸�ȫ�ֱ���
         async:true,
         cache:false,
         // ���̨����data��Ĳ���
         data:{
         'start': start,
         'end': end,
         // ע��: �����������, ��Ҫjson��
         'code_lst': JSON.stringify(code_lst)
         },
         dataType:'json',
         // �����������, ��Ҫ��traditional: true
         traditional: true,
         // ���سɹ�, ִ�к���
         success:function(res){
              var series = [];
              // �����ص�ֵpush��series������
              for (var i = 0; i < code_lst.length; i++) {
                      series.push({
                                type:'line',
                                // series��nameҪ��legend.data����һ��
                                name: code_lst[i],
                                data: res[code_lst[i]]
                          });
                    };
              option.xAxis.data = res.xlab;
              option.series = series;
              option.legend.data = code_lst;
              // ����Ϊtrue�ɴ���������������
              myChart1.setOption(option, true);

               }
         });

    // ��������
    myChart1.on('datazoom', function (params) {
      // �õ����ŵ���ֹ����
      var startX = myChart1.getOption().dataZoom[0].endValue;
      var endX = myChart1.getOption().dataZoom[0].startValue;
      var endTime = option.xAxis.data[startX];
      var startTime = option.xAxis.data[endX];

      code = xmSelect.get('#code_lst1', true);
      code_lst = code.getValue('name');

      $.ajax({
         type:'get',
         // ͨ��url������ͼ����
         url:'./portfolioReturn/get_start_end',
         // async:true �첽���� ��ʱ���޸�ȫ�ֱ���
         async:true,
         cache:false,
         data:{
         'start': startTime,
         'end': endTime,
         // ע��: �����������, ��Ҫjson��
         'code_lst': JSON.stringify(code_lst)
         },
         dataType:'json',
         // �����������, ��Ҫ��traditional: true
         traditional: true,
         // ���سɹ�, ִ�к���
         success:function(res){
              var series = []
              // ��ʱֻ���޸�series�������data
              for (var i = 0; i < code_lst.length; i++) {

                      series.push({
                                type:'line',
                                name: code_lst[i],
                                data: res[code_lst[i]]
                          });
                    };
                // Ӧ��option ����myChart.setOption({})�޸������series
                myChart1.setOption({
                series: series
          });
             }
         });

        });
    // �ύ����ˢ��
    return false;
  });


});



// ��ϻ�׼�Աȱ�
layui.use('form', function(){
// ������
var form = layui.form;

// ����ͼ
var myChart2 = echarts.init(document.getElementById('portfolio_graph2'));
    // ��ʾ���⣬ͼ���Ϳյ��������ͼ����
    var option = {
        title: {
            text: ''
        },
        // ��ʾ��
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                    type: 'cross'
                },
            position: function (pt) {
                return [pt[0], '10%'];
            },
            // ��ʾ���ʽת��Ϊ�ٷֺ�
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
        // ͼ��
        legend: {
                top: 10,
                left: 'center',

                data: []
            },
        xAxis: {
            data: []
        },
        // Y������ת��Ϊ�ٷֺ�
        yAxis: {
        axisLabel:{
                        formatter:function (value, index) {
        return (value*100).toFixed(0)+'%';
                                               }
                   }
        },
        // ����������
        dataZoom: [
            {   // ���dataZoom�����Ĭ�Ͽ���x�ᡣ
                type: 'slider', // ��� dataZoom ����� slider �� dataZoom ���
                start: 0,      // ����� 10% ��λ�á�
                end: 100         // �ұ��� 60% ��λ�á�
            }
        ],
        // ÿ��ϵ��ͨ�� type �����Լ���ͼ������
        series: [
        ]
    };

    // Ӧ��option
    myChart2.setOption(option);

    // �����ύ ͨ��button���lay-filter='formDemo2'����
  form.on('submit(formDemo2)', function(res){
    // ͨ��������res.field�õ���ֹʱ��
    var start = res.field.start;
    var end = res.field.end;
    var code = xmSelect.get('#code_lst2', true);
    var code_lst = code.getValue('name');
    var index = xmSelect.get('#index_lst1', true);
    var index_lst = index.getValue('name');


    // �õ���ѡ���е��ַ�������


    $.ajax({
        type:'get',
         // ͨ��url������ͼ����
         url:'./portfolioReturn/get_start_end_index',
         // async:true �첽���� ��ʱ���޸�ȫ�ֱ���
         async:true,
         cache:false,
         // ���̨����data��Ĳ���
         data:{
         'start': start,
         'end': end,
         'code': JSON.stringify(code_lst),
         // ע��: �����������, ��Ҫjson��
         'index_lst': JSON.stringify(index_lst)
         },
         dataType:'json',
         // �����������, ��Ҫ��traditional: true
         traditional: true,
         // ���سɹ�, ִ�к���
         success:function(res){
              var series = [];
              series.push({
                                type:'line',
                                // series��nameҪ��legend.data����һ��
                                name: code_lst[0],
                                data: res[code_lst[0]]
              });

              for (var i = 0; i < index_lst.length; i++) {
                      series.push({
                                type:'line',
                                // series��nameҪ��legend.data����һ��
                                name: index_lst[i],
                                data: res[index_lst[i]]
                          });
                      code_lst.push(index_lst[i])

                    };

              option.xAxis.data = res.xlab;
              option.series = series;
              option.legend.data = code_lst;
              // ����Ϊtrue�ɴ���������������

              myChart2.setOption(option, true);

               }
         });



    // ��������
    myChart2.on('datazoom', function (params) {
      // �õ����ŵ���ֹ����
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
         // ͨ��url������ͼ����
         url:'./portfolioReturn/get_start_end_index',
         // async:true �첽���� ��ʱ���޸�ȫ�ֱ���
         async:false,
         cache:false,
         data:{
         'start': startTime,
         'end': endTime,
         'code': JSON.stringify(code_lst),
         // ע��: �����������, ��Ҫjson��
         'index_lst': JSON.stringify(index_lst)
         },
         dataType:'json',
         // �����������, ��Ҫ��traditional: true
         traditional: true,
         // ���سɹ�, ִ�к���
         success:function(res){
              var series = [];

              series.push({
                                type:'line',
                                // series��nameҪ��legend.data����һ��
                                name: code_lst[0],
                                data: res[code_lst[0]]
              });

              for (var i = 0; i < index_lst.length; i++) {
                      series.push({
                                type:'line',
                                // series��nameҪ��legend.data����һ��
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
    // �ύ����ˢ��
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






















