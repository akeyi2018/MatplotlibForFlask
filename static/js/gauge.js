var randomScalingFactor = function() {
    return Math.round(Math.random() * 100);
  };
  
//   var randomData = function () {
//     return [
//       randomScalingFactor(),
//       randomScalingFactor(),
//       randomScalingFactor(),
//       randomScalingFactor()
//     ];
//   };
  
//   var randomValue = function (data) {
//     return Math.max.apply(null, data) * Math.random();
//   };
  
//   var data = randomData(); //デフォルト
//   console.log(data);
  // R/1 Y/2 G/3 B/4
//   var data = [10, 20, 30, 40];
     var data = [8, 22, 33, 40];

//   var value = randomValue(data);
//   console.log(value);
  var value = 28.4
  
  var config = {
    type: 'gauge',
    data: {
      //labels: ['Success', 'Warning', 'Warning', 'Error'],
      datasets: [{
        data: data,
        value: value,
        backgroundColor: ['blue', 'green', 'orange', 'red'],
        // borderWidth: 2 //デフォルト
        borderWidth: 1 
      }]
    },
    options: {
      responsive: true,
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
        color: 'rgba(125, 89, 213, 1)'
      },
      valueLabel: {
        formatter: Math.round
      }
    }
  };
  
  window.onload = function() {
    var ctx = document.getElementById('chart').getContext('2d');
    window.myGauge = new Chart(ctx, config);
  };
  
  document.getElementById('randomizeData').addEventListener('click', function() {
    config.data.datasets.forEach(function(dataset) {
    //   dataset.data = randomData();
        dataset.data = [50, 50, 50, 50];
    //   dataset.value = randomValue(dataset.data);
        dataset.value = 50;
    });
  
    window.myGauge.update();
  });