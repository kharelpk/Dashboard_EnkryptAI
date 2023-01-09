// SIDEBAR TOGGLE

var sidebarOpen = true;

var sidebar = document.getElementById("sidebar");

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.remove("sidebar-minimized");
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.add("sidebar-minimized");
    sidebarOpen = false;
  }
}

// ------------------ DATASET ----------------------------

// ------------ CHARTS ----------------------

// var barChartOptions = {
//   series: [
//     {
//       data: [1380, 1200, 690, 540, 448],
//     },
//   ],
//   chart: {
//     type: "bar",
//     height: 350,
//     toolbar: {
//       show: false,
//     },
//   },
//   //   colors: ["#246dec", "#cc3c43", "#367952", "#f5b74f", "#4f35a1"],
//   plotOptions: {
//     bar: {
//       distributed: true,
//       borderRadius: 4,
//       horizontal: true,
//       columnWidth: "40%",
//     },
//   },
//   tooltip: {
//     enabled: false,
//   },
//   dataLabels: {
//     enabled: false,
//   },
//   legend: {
//     show: false,
//   },

//   xaxis: {
//     categories: [
//       "Statistics",
//       "Visualization",
//       "Encryption",
//       "Training",
//       "Inference",
//     ],
//     axisTicks: {
//       show: false,
//     },
//     labels: {
//       show: false,
//       style: {
//         fontSize: "14px",
//         fontFamily: "Source Sans Pro",
//         color: "#696969",
//       },
//     },
//   },

//   dataLabels: {
//     style: {
//       fontSize: "14px",
//       fontWeight: "Thin",
//       fontFamily: "Source Sans Pro",
//       color: "#696969",
//     },
//   },

//   yaxis: {
//     labels: {
//       style: {
//         fontSize: "14px",
//         fontFamily: "Source Sans Pro",
//         color: "#696969",
//       },
//     },
//   },
//   grid: {
//     show: false,
//   },
// };

// var chart = new ApexCharts(
//   document.querySelector("#bar-chart"),
//   barChartOptions
// );
// chart.render();

// --------- PIE CHART -----------------
var pieChartOptions = {
  chart: {
    height: 350,
    type: "radialBar",
  },

  series: [88],

  plotOptions: {
    radialBar: {
      hollow: {
        margin: 15,
        size: "70%",
      },

      dataLabels: {
        showOn: "always",
        name: {
          offsetY: -10,
          show: true,
          fontSize: "14px",
          fontFamily: "Source Sans Pro",
          color: "#696969",
          fontWeight: "Thin",
        },
        value: {
          color: "#111",
          fontSize: "30px",
          show: true,
        },
      },
    },
  },

  stroke: {
    lineCap: "round",
  },
  labels: ["Uptime"],
};

var pieChart = new ApexCharts(
  document.querySelector("#pie-chart"),
  pieChartOptions
);

pieChart.render();

// ------------------ Chart visualization ----------------------------

// var yData = [5, 8, 24, 16, 32, 42, 30, 17, 11];
// var options = {
//   chart: {
//     type: "bar",
//   },
//   series: [
//     {
//       name: "visitors",
//       data: Array.from({ length: yData.length }, (_, i) => ({
//         x: 0.5 + i,
//         y: yData[i],
//         ...(i === 4
//           ? { fillColor: "rgba(32, 120, 255, 0.4)", strokeColor: "#80afff" }
//           : {}),
//       })),
//     },
//   ],
//   plotOptions: {
//     bar: {
//       columnWidth: "95%",
//       strokeWidth: 2,
//       borderRadius: 5,
//       borderRadiusApplication: "end",
//     },
//   },
//   fill: {
//     colors: "#ff4040",
//     opacity: 0.3,
//   },
//   stroke: {
//     width: 2,
//     colors: ["#ee8080"],
//   },
//   dataLabels: { enabled: false },
//   grid: {
//     xaxis: {
//       lines: {
//         show: true,
//       },
//     },
//     yaxis: {
//       lines: {
//         show: true,
//       },
//     },
//   },
//   xaxis: {
//     type: "numeric",
//     min: 0,
//     max: yData.length,
//     tickAmount: yData.length,
//     labels: { formatter: (x) => x /*Math.round(x)*/ },
//     title: { text: "Hours", offsetY: 70 },
//     axisBorder: {
//       color: "#000000",
//     },
//   },
//   yaxis: {
//     title: { text: "Visitors" },
//     min: 0,
//     max: Math.max(...yData),
//     axisBorder: {
//       show: true,
//       color: "#000000",
//     },
//   },
//   tooltip: {
//     onDatasetHover: {
//       highlightDataSeries: true,
//     },
//     x: {
//       formatter: (x) => {
//         return "Hours " + (x - 0.5) + "-" + (x + 0.5);
//       },
//     },
//   },
// };

// var chart_viz = new ApexCharts(
//   document.querySelector("#chart-viz-page"),
//   options
// );
// chart_viz.render();
