// apps/aiengine/assets/js/aiengine_dashboard.js

document.addEventListener('DOMContentLoaded', function() {
  var options = {
      chart: { type: 'line' },
      series: [{ name: 'Performance', data: performance_data }],
      xaxis: { categories: performance_dates }
  };
  var chart = new ApexCharts(document.querySelector("#metrics-chart"), options);
  chart.render();
});
