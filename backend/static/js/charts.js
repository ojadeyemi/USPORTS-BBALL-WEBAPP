// Function to show the radar chart with specified teams
function showRadarChart(team1, team2) {
  // Get the canvas element
  const ctx = document.getElementById("radarChart").getContext("2d");

  // Define data valeus and its attributes
  const data = {
    labels: ["Overall", "Defense", "Playmaking", "Rebounding", "Efficiency", "Offense"], // Update labels as needed
    datasets: [
      {
        label: team1, // Update label based on selected team 1
        data: radarData[team1], // Update data based on selected team 1
        fill: true,
        backgroundColor: "rgba(255, 99, 132, 0.3)",
        borderColor: "rgb(255, 99, 132)",
        pointBackgroundColor: "rgb(255, 99, 132)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgb(255, 99, 132)",
        borderWidth: 3,
      },
      {
        label: team2, // Update label based on selected team 2
        data: radarData[team2], // Update data based on selected team 2
        fill: true,
        backgroundColor: "rgba(54, 162, 235, 0.3)",
        borderColor: "rgb(54, 162, 235)",
        pointBackgroundColor: "rgb(54, 162, 235)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgb(54, 162, 235)",
        borderWidth: 3,
      },
    ],
  };

  // Defining options
  const options = {
    normalized: true,
    interaction: {
      mode: "index", // Sets the interaction mode. Options: 'nearest', 'point', 'index', 'dataset'
    },
    plugins: {
      //Title configuration
      title: {
        display: false,
        text: "",
      },
      // Legend configuration
      legend: {
        display: true, // Determines if the legend should be displayed
        position: "top", // Position of the legend. Options: 'top', 'bottom', 'left', 'right'
        align: "center", // Alignment of the legend. Options: 'start', 'center', 'end'

        labels: {
          color: "#fff",
          boxWidth: 50, //width of legend label box
        },
      },
    },
    scales: {
      r: {
        min: 40,
        max: 100,
        ticks: {
          display: false,
          stepSize: 10,
          backdropPadding: 5,
          font: {
            size: 10, // Size of the font
            style: "normal", // Style of the font
            family: "Helvetica", // Family of the font
            weight: "normal", // Weight of the font
          },
        },
        grid: {
          circular: false,
          offset: true,
          color: "#808080",
        },
        angleLines: {
          color: "#bfbfbf",
        },
        pointLabels: {
          color: "#fff",
          fontSize: 10,
        },
      },
    },
  };

  // Radar chart configuration
  const config = {
    type: "radar",
    data: data,
    options: options,
  };

  // Create radar chart
  const myRadarChart = new Chart(ctx, config);

  return myRadarChart; // Return the chart instance
}

// Get selected team names
const team1Element = document.getElementById("team1-select");
const team2Element = document.getElementById("team2-select");

// Add event listener to the select element
team1Element.addEventListener("change", selectTeam);
team2Element.addEventListener("change", selectTeam);

// Define the variables team1 and team2 outside the function
var team1;
var team2;

document.addEventListener("DOMContentLoaded", () => {
  // Initially show the radar chart with default teams
  radarChart = showRadarChart("Acadia", "Acadia");
});

function selectTeam() {
  team1 = team1Element.value;
  team2 = team2Element.value;

  // Update the radar chart with selected teams
  radarChart.data.datasets[0].label = team1;
  radarChart.data.datasets[0].data = radarData[team1];
  radarChart.data.datasets[1].label = team2;
  radarChart.data.datasets[1].data = radarData[team2];

  // Update the chart
  radarChart.update();
}
