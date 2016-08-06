function Game(gameType, gameDiv) {
  this.div = gameDiv;
  this.gameType = gameType;
  this.players = [];
}

Game.prototype = {
  constructor: Game,

  addPlayer: function(playerName) {
    this.player.push(playerName);
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
  prepareForSubmission: function() {
    $('#submit-game').click(function() {
      // TODO show page for player data
      console.log('Game submitted');
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
    this.div.html(html);
    this.setUpPlayerSelect();
  }
};
