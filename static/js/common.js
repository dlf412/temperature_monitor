// 实名认证 通用option
var realPeopelOption = {
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/> ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data: ['实名认证比例'],
        show: false
    },
    color: ['#0685FA'],
    series: [
        {
            name: '实名认证比例',
            type: 'pie',
            radius: ['70%', '90%'],
            avoidLabelOverlap: false,
            label: {
                normal: {
                    show: true,
                    position: 'center',
                    textStyle: {
                        fontSize: '20',
                        fontWeight: 'bold'
                    },
                    formatter: function () {
                        var str = "100%";
                        return str;
                    }
                }
            },
            hoverAnimation: false,
            labelLine: {
                normal: {
                    show: false
                }
            },
            data: [{ value: 100 }]
        }
    ]
};


