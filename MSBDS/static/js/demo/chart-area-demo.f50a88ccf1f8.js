// Dummy data for infestation trend
var infestationData = [10, 20, 30, 25, 35, 40, 45, 50, 55, 60, 65, 70];

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
      label: "Infestation Trend",
      lineTension: 0.3,
      backgroundColor: "rgba(255, 99, 132, 0.05)",
      borderColor: "rgba(255, 99, 132, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(255, 99, 132, 1)",
      pointBorderColor: "rgba(255, 99, 132, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(255, 99, 132, 1)",
      pointHoverBorderColor: "rgba(255, 99, 132, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: infestationData,
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10,
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': ' + tooltipItem.yLabel + ' infestations';
        }
      }
    }
  }
});
