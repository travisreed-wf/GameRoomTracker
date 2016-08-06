function Game(gameType, gameDiv) {
  this.div = gameDiv;
  this.gameType = gameType;
  this.players = [];
}

Game.prototype = {
  constructor: Game,

  addPlayer: function(playerName) {
    this.players.push(playerName);
  },
  getOptionsHTML: function() {
    var html =
      '<hr />' +
      '<h4>Set options</h4>' +
      '<div class="checkbox">' +
        '<label>' +
          '<input id="ranked-checkbox" type="checkbox" checked/> Ranked Game' +
        '</label>' +
      '</div>' +
      '<select id="select-players" multiple="multiple">' +
        '<option></option>' +
        '<option>Dave Eickelberg</option>' +
        '<option>Jeremy Curtiss</option>' +
        '<option>Joe McGovern</option>' +
        '<option>Luke Van Gorp</option>' +
        '<option>Travis Reed</option>' +
      '</select>' +
      '<div style="margin-top:1em">' +
        '<button id="submit-game" class="btn btn-primary" type="button">Add game</button>' +
      '</div>';
    return $(html);
  },
  handleSubmission: function() {
    // TODO check that there is at least two
    var playerNames = $('#select-players').val();
    for (var i = 0; i < playerNames.length; i++) {
      var player = new Player(playerNames[i]);
      this.addPlayer(player);
    }
    this.showNextPlayerPage();
  },
  setUpSubmissonHandler: function() {
    var _this = this;
    $('#submit-game').click(function() {
      _this.handleSubmission();
    });
  },
  setUpPlayerSelect: function() {
    $('#select-players').select2({
      placeholder: 'Select players',
      width: '100%'
    });
  },
  showOptions: function() {
    var html = this.getOptionsHTML();
    this.div.find('#options').html(html);
    this.setUpPlayerSelect();
  },
  showNextPlayerPage: function() {
    var player = this.players.shift();
    var html = player.getHTML();
    this.div.html(html);
    player.setUpSubmissonHandler();
  }
};
