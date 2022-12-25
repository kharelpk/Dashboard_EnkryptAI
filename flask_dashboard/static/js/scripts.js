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

// ------------ CHARTS ----------------------

var barChartOptions = {
  series: [
    {
      data: [1380, 1200, 690, 540, 448],
    },
  ],
  chart: {
    type: "bar",
    height: 350,
    toolbar: {
      show: false,
    },
  },
  //   colors: ["#246dec", "#cc3c43", "#367952", "#f5b74f", "#4f35a1"],
  plotOptions: {
    bar: {
      distributed: true,
      borderRadius: 4,
      horizontal: true,
      columnWidth: "40%",
    },
  },
  tooltip: {
    enabled: false,
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: false,
  },

  xaxis: {
    categories: [
      "Statistics",
      "Visualization",
      "Encryption",
      "Training",
      "Inference",
    ],
    axisTicks: {
      show: false,
    },
    labels: {
      show: false,
      style: {
        fontSize: "14px",
        fontFamily: "Source Sans Pro",
        color: "#696969",
      },
    },
  },

  dataLabels: {
    style: {
      fontSize: "14px",
      fontWeight: "Thin",
      fontFamily: "Source Sans Pro",
      color: "#696969",
    },
  },

  yaxis: {
    labels: {
      style: {
        fontSize: "14px",
        fontFamily: "Source Sans Pro",
        color: "#696969",
      },
    },
  },
  grid: {
    show: false,
  },
};

var chart = new ApexCharts(
  document.querySelector("#bar-chart"),
  barChartOptions
);
chart.render();

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
