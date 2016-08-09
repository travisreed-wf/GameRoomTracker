game = null;
gUsernames = [];
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
      gUsernames = JSON.parse(data);
    },
    error: function() {
      // TODO feedback
      console.error('Bad request');
    }
  });
}
