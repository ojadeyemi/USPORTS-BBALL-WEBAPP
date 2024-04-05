document.addEventListener("DOMContentLoaded", showRadarChart);

function showRadarChart() {
  console.log(radarData); //figure out how to select specify teams

  // Extract team names and radar data values
  const teamNames = Object.keys(radarData);
  const radarValues = Object.values(radarData);

  // Get the canvas element
  const ctx = document.getElementById("radarChart").getContext("2d");

  // Radar chart configuration
  const config = {
    type: "radar",
    data: {
      labels: ["Overall", "Offense", "Defense", "Playmaking", 'Rebounding'], // Update labels as needed
      datasets: [
        {
          label: teamNames[44], // Update label based on team names
          data: radarValues[44], // Update data based on radar values
          fill: true,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgb(255, 99, 132)",
          pointBackgroundColor: "rgb(255, 99, 132)",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "rgb(255, 99, 132)",
          borderWidth: 2,
        },
        {
          label: teamNames[42], // Update label based on team names
          data: radarValues[42], // Update data based on radar values
          fill: true,
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          borderColor: "rgb(54, 162, 235)",
          pointBackgroundColor: "rgb(54, 162, 235)",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "rgb(54, 162, 235)",
          borderWidth: 2,
        },
      ],
    },
    options: {
      elements: {
        line: {
          borderWidth: 5,
        },
      },
      scales: {
        r: {
            min: 0,
            max: 100,
            ticks: {
                display : false,
            },
        }
    },
},
};

  // Create radar chart
  var myRadarChart = new Chart(ctx, config);
}
