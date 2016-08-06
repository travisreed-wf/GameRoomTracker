game = null;
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
