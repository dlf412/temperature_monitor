$(document).ready(function(){
    //实名认证饼图
    var realPeopleChart = echarts.init(document.getElementById("realPeople"));
    var options = realPeopelOption;//common.js
    realPeopleChart.setOption(options);

    window.onresize = function () {
        realPeopleChart.resize();
    };
});