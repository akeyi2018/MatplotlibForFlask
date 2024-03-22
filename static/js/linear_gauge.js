var barChartData10 = {labels: [], datasets: []};
barChartData10.datasets.push({
    data: [76.3],
    pointer: 'point',  //現在のポイント（計測点）
    shape: 'triangle',
    width: 18,
    height: 30,
    offset: 8,
    backgroundColor: '#1b02f7',
    //ゲージの色と境界線
    colorRanges: [{startpoint: 60,breakpoint: 68,color: '#31d801'},
                {startpoint: 68,breakpoint: 81,color: '#e1e10d'}, {
        startpoint: 81,
        breakpoint: 90,
        color: '#d90000'
    }]
});

window.onload = function() {
    var ctx10 = document.getElementById("canvas10").getContext("2d");
    window.myBar10 = new Chart(ctx10, {
        type: 'linearGauge',
        data: barChartData10,
        options: {
            responsive: false,
            title:{
                display: false,
                text: 'weight'
            },
            scale: {
                horizontal: true,
                range: {startValue: 60,endValue: 90},
                responsive: false,
                font: {
                    fontName: 'Arial',
                    fontSize: 14
                },
                axisWidth: 10,
                axisColor: '#c5c7cf',
                ticks: {
                     majorTicks: {
                        interval: 1,
                        width: 8,
                        height: 1,
                        offset: 1,
                        color: '#000'
                    },
                    minorTicks: {
                        interval: .2,
                        width: 3,
                        height: 1,
                        offset: 0,
                        color: '#000'
                    },
                },
                scaleLabel: {
                    display: true,
                    interval: 5,
                    units: 'kg',
                    offset: -17,
                    color: '#0f0f0f'
                },
                scaleColorRanges: [
                {
                    start: 60,
                    end: 68,
                    color: '#47fe12'
                }, {
                    start: 68,
                    end: 81,
                    color: '#e1e10d'
                }, {
                    start: 81,
                    end: 90,
                    color: '#fe1229'
                }],
            },
            legend: {
                display: false,
                position: ''
            }}
    });
};