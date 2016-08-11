feedback = null;
game = null;
gUsernames = [];
fetchUsernames();
$(document).ready(function() {
  feedback = new Feedback($('#home-page-feedback'));
  game = new Game($('#game'));
  game.createInitialView();
});



function fetchUsernames() {
  $.ajax({
    url: '/api/user/usernames/',
    method: 'GET',
    success: function(data) {
      gUsernames = JSON.parse(data);
      game.enableGameSelect();
    },
    error: function() {
      var m = 'Could not fetch players. Please reload page.';
      feedback.alert(m, 'red');
    }
  });
}
