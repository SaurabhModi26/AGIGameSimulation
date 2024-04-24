// Get the canvas element
var canvas = document.getElementById('gameCanvas');
var ctx = canvas.getContext('2d');

// Send an AJAX request to the server to start the game
function startGame() {
    var xhttp = new XMLHttpRequest();
    xhttp.open('GET', '/start_game', true);
    xhttp.send();
}

// Event listener for when the webpage finishes loading
window.addEventListener('load', function() {
    startGame();
});
