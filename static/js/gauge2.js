var value = 10;
var data = [0, 0, value, 20];

// 体重分布
// var data = [8, 22, 33, 40];
// var value = 10
  
  var config = {
    type: 'gauge',
    data: {
      labels: ['1', '2', '3', '4'],
      datasets: [{
        data: data,
        value: value,
        // backgroundColor: ['blue', 'green', 'orange', 'red'],
        backgroundColor: ['blue', 'green', 'blue', '#ffffff'],
        // borderWidth: 2 //デフォルト
        borderWidth: 1 
      }]
    },
    options: {
      responsive: false,
      title: {
        display: true,
        text: '体重'
      },
      layout: {
        padding: {
          bottom: 30
        }
      },
      needle: {
        // Needle circle radius as the percentage of the chart area width
        // radiusPercentage: 2, //デフォルト
        radiusPercentage: 0.5,
        // Needle width as the percentage of the chart area width
        // widthPercentage: 3.2,　//デフォルト
        widthPercentage: 1.0,
        // Needle length as the percentage of the interval between inner radius (0%) and outer radius (100%) of the arc
        // lengthPercentage: 80,　//デフォルト
        lengthPercentage: 70,　
        // The color of the needle
        // color: 'rgba(125, 89, 213, 1)'
        color: '#ffffff'
      },
      valueLabel: {
        formatter: Math.round
      }
    }
  };
  
  window.onload = function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    window.myGauge = new Chart(ctx, config);
  };
  
  