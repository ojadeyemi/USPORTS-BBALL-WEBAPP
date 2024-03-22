document
  .getElementById("playerAnalyticsBtn")
  .addEventListener("click", showPlayerAnalytics);

// Event listeners for navigation buttons or links
document
  .getElementById("standingsBtn")
  .addEventListener("click", showStandings);

document
  .getElementById("conference-filter")
  .addEventListener("change", filterStandingsByConf);

document
  .getElementById("leaderboardBtn")
  .addEventListener("click", showLeaderboard);

document
  .getElementById("teamanalyticsBtn")
  .addEventListener("click", showTeamAnalytics);

// Function to show standings section
function showStandings() {
  var standingsSection = document.getElementById("standings-section");
  var leaderboardSection = document.getElementById("playerleaderboard-section");
  var teamanalyticsSection = document.getElementById("teamanalytics-section");
  var playeranalyticsSection = document.getElementById(
    "playeranalytics-section"
  );

  // Set the display property to "block" to show the standings section
  standingsSection.style.display = "block";

  // Set the display property to "none" to show the teamanalytics section
  teamanalyticsSection.style.display = "none";

  // Set the display property to "none" to show the leaderboard section
  leaderboardSection.style.display = "none";
  playeranalyticsSection.style.display = "none";
}

// Function to filter standings by conference
function filterStandingsByConf() {
  var selectedConference = document.getElementById("conference-filter").value;
  var teams = document.getElementsByClassName("team");
  for (var i = 0; i < teams.length; i++) {
    var team = teams[i];
    if (
      selectedConference === "all" ||
      team.classList.contains(selectedConference)
    ) {
      team.style.display = "flex";
    } else {
      team.style.display = "none";
    }
  }
}

// Function to show leaderboard senone
function showLeaderboard() {
  var standingsSection = document.getElementById("standings-section");
  var leaderboardSection = document.getElementById("playerleaderboard-section");
  var teamanalyticsSection = document.getElementById("teamanalytics-section");
  var playeranalyticsSection = document.getElementById(
    "playeranalytics-section"
  );
  // Set the display property to "block" to show the leaderboard section
  leaderboardSection.style.display = "block";
  // Set the display property to "none" to show the teamanalytics section
  teamanalyticsSection.style.display = "none";

  // Set the display property to "none" to show the standings section
  standingsSection.style.display = "none";

  playeranalyticsSection.style.display = "none";
}

// Function to show team analytics section
function showTeamAnalytics() {
  var standingsSection = document.getElementById("standings-section");
  var leaderboardSection = document.getElementById("playerleaderboard-section");
  var teamanalyticsSection = document.getElementById("teamanalytics-section");
  var playeranalyticsSection = document.getElementById(
    "playeranalytics-section"
  );
  //Set the display to show team analytics
  teamanalyticsSection.style.display = "block";
  // Set the display property to "none" to show the leaderboard section
  leaderboardSection.style.display = "none";

  // Set the display property to "none" to show the standings section
  standingsSection.style.display = "none";

  playeranalyticsSection.style.display = "none";
}

// Function to show team analytics section
function showPlayerAnalytics() {
  var standingsSection = document.getElementById("standings-section");
  var leaderboardSection = document.getElementById("playerleaderboard-section");
  var teamanalyticsSection = document.getElementById("teamanalytics-section");
  var playeranalyticsSection = document.getElementById(
    "playeranalytics-section"
  );

  // Set the display property to "none" to show the leaderboard section
  leaderboardSection.style.display = "none";

  // Set the display property to "none" to show the standings section
  standingsSection.style.display = "none";

  //Set the display to show team analytics
  teamanalyticsSection.style.display = "none";

  playeranalyticsSection.style.display = "block";
}
