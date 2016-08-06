game = null;
USERNAMES = [];
fetchUsernames();
$(document).ready(function() {
  game = new Game($('#game'));
  game.createInitialView();
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
