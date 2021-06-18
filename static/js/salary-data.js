$(document).ready(function(){
    //薪资发放折线图  /*后端数据 dataX-x轴数据 dataY-y轴数据*/
    var dataX = ['2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10'];
    var dataY = [44, 33, 27, 50, 61, 41, 39, 44, 33, 27];
    var salaryChart = echarts.init(document.getElementById("salaryChart"));
    var options1 = {
        title: {
            text: '薪资发放情况',
            textStyle: {
                fontSize: 16
            },
            top: 10
        },
        toolbox: {
            feature: {
                saveAsImage: { show: true },
                magicType: {
                    type: ['line', 'bar']
                }
            }
        },
        tooltip: {
            trigger: 'axis',
            formatter: "{a} <br/> {b} , {c}" + '元'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        //calculable: true,
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: dataX
            }
        ],
        yAxis: [
            {
                type: 'value',
                splitLine: {
                    show: false
                }
            }
        ],
        series: [
            {
                name: '薪资发放金额',
                type: 'line',
                stack: '总量',
                smooth: true,
                symbol: 'none',
                areaStyle: {
                    normal: {
                        color: '#A4EBFF',
                        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
                            offset: 0, color: '#A5F1FF' // 0% 处的颜色
                        }, {
                            offset: 0.25, color: '#A5ECFF'
                        }, {
                            offset: 0.5,
                            color: '#A6E1FF'
                        }, {
                            offset: 0.75,
                            color: '#A5D9FF'
                        }, {
                            offset: 1,
                            color: '#A6D5FF' // 100% 处的颜色
                        }], false)
                    }
                },
                lineStyle: {
                    normal: {
                        width: 3,
                        //shadowColor: 'rgba(255,255,255,.8)',
                        //shadowBlur: 10,
                        //shadowOffsetY: 1,
                        //shadowOffsetX: 2,
                        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
                            offset: 0, color: '#26D4F3' // 0% 处的颜色
                        }, {
                            offset: 1, color: '#1083ED' // 100% 处的颜色
                        }], false)
                    }
                },
                data: dataY
            }
        ]
    }
    salaryChart.setOption(options1);

    window.onresize = function () {
        salaryChart.resize();
    };
});