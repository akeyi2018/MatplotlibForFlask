var data = {
  labels: [
    "Red"
  ],
  datasets: [
    {
      data: [75],
      backgroundColor: [
        "#FF6384",
        "#36A2EB",
        "#FFCE56"
      ],
      hoverBackgroundColor: [
        "#FF6384",
        "#36A2EB",
        "#FFCE56"
      ]
    }
  ]
};

// キャンバス要素を取得
var ctx = document.getElementById("myChart");

// And for a doughnut chart
var myDoughnutChart = new Chart(ctx, {
  type: 'doughnut',
  data: data,
  options: {
    rotation: 1 * Math.PI,
    circumference: 1 * Math.PI,
    // キャンバスのサイズを設定
    responsive: false,
    maintainAspectRatio: false
  }
});