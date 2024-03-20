document.getElementById('conference-filter').addEventListener('change', function() {
    var selectedConference = this.value;
    var teams = document.getElementsByClassName('team');
    for (var i = 0; i < teams.length; i++) {
        var team = teams[i];
        if (selectedConference === 'all' || team.classList.contains(selectedConference)) {
            team.style.display = 'flex';
        } else {
            team.style.display = 'none';
        }
    }
});