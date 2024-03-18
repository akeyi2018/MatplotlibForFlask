document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('myChart');
    new Chart(ctx, {
        type: 'line',
        data: {
        labels: healthDataDate,
        datasets: [{
            label: '最高血圧',
            data: healthDataHigh,
            borderColor: '#FF1493',
            backgroundColor: '#FF69B4',
            lineTension:0.2,
            yAxisID: 'y',
            }, {
            label: '最低血圧',
            data: healthDataLow,
            borderColor: '#EE82EE',
            backgroundColor: '#DDA0DD',
            lineTension:0.2,
            yAxisID: 'y',
            },{
            label: '心拍数',
            data: healthDataPulse,
            
            borderColor: '#FF7f8F',
            backgroundColor: '#FFBFCF',
            lineTension:0.2,
            yAxisID: 'y',
            },{
            label: '体重',
            data: healthDataWeight,
            borderColor: '#7CFC00',
            backgroundColor: '#ADFF2F',
            lineTension:0.2,
            yAxisID: 'y2',
            }
        ]
        },
        options: {
        responsive: true,
        maintainAspectRatio: true, 
        interaction: {
            mode: 'index',
            intersect: false,
            },
        stacked: false,
        plugins: {
        title: {
            display: true,
            text: '血圧と体重管理'
        }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'week',
                    displayFormats:{
                        week: 'MM月dd日'
                    }
                }
            },
            y: {
                position: 'left',
                min: 60,
                max: 180,
                title: {
                    text: '血圧(mm/Hg)',
                    display: true,
                },
                
            },
            y2: {
                position: 'right',
                min: 70,
                max: 80,
                title: {
                    text: '体重(kg)',
                    display: true,
                },
                
                // grid line settings
                grid: {
                drawOnChartArea: false, // only want the grid lines for one axis to show up
                },
            },
        }
        }
    });

});