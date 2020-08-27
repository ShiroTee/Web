// js �õ��Ŀ��: layui, echarts
// layui �ĵ���ַ: https://www.layui.com/doc/
// echarts �ĵ���ַ: https://echarts.apache.org/zh/option.html#title
// ע��: ��Ҫ��base.html����layui��css, js�ļ�, echarts��css, js�ļ�, xm-select��js�ļ�


layui.use('form', function(){
// ������
var form = layui.form;

// ����ͼ
var myChart = echarts.init(document.getElementById('portfolio_graph1'));
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
    myChart.setOption(option);



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
         url:'/correct/graph1/get_start_end',
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
              for (i = 0; i < code_lst.length; i++) {
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
              myChart.setOption(option, true);

               }
         });

    // ��������
    myChart.on('datazoom', function (params) {
      // �õ����ŵ���ֹ����
      var startX = myChart.getOption().dataZoom[0].endValue;
      var endX = myChart.getOption().dataZoom[0].startValue;
      var endTime = option.xAxis.data[startX];
      var startTime = option.xAxis.data[endX];

      code = xmSelect.get('#code_lst1', true);
      code_lst = code.getValue('name');

      $.ajax({
         type:'get',
         // ͨ��url������ͼ����
         url:'/correct/graph1/get_start_end',
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
              for (i = 0; i < code_lst.length; i++) {

                      series.push({
                                type:'line',
                                name: code_lst[i],
                                data: res[code_lst[i]]
                          });
                    };
                // Ӧ��option ����myChart.setOption({})�޸������series
                myChart.setOption({
                series: series
          });
             }
         });

        });
    // �ύ����ˢ��
    return false;
  });


});