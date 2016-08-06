game = null;
USERNAMES = [];
fetchUsernames();
$(document).ready(function() {
  var gameSelectDiv = $('#game-select');
  gameSelectDiv.select2({
    placeholder: 'Select a game'
  });

  $('#game-select').on('change', function() {
    var select = $(this);
    var gameType = select.val();
    game = new Game(gameType, $('#game'));
    game.showOptions();
    game.setUpSubmissonHandler();
  });
});


function fetchUsernames() {
  $.ajax({
    url: '/api/user/usernames/',
    method: 'GET',
    success: function(data) {
      USERNAMES = JSON.parse(data);
    },
    error: function() {
      // TODO feedback
      console.error('Bad request');
    }
  });
}
