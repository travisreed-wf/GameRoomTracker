function Game(gameType, gameDiv) {
  this.div = gameDiv;
  this.gameType = gameType;
  this.players = [];
  this.playerIndex = 0;
  this.isRanked = null;
}

Game.prototype = {
  constructor: Game,

  addGameToDatastore: function() {
    var _this = this;
    var requestData = this.prepareRequest();
    $.ajax({
      url: '/api/game/',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(requestData),
      success: function() {
        _this.showSuccessfulPage();
      },
      error: function() {
        // TODO show some feedback
        console.error('error');
      }
    });
  },
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
        this.getUserNamesHTML() +
      '</select>' +
      '<div style="margin-top:1em">' +
        '<button id="submit-game" class="btn btn-primary" type="button">Add game</button>' +
      '</div>';
    return $(html);
  },
  getUserNamesHTML: function() {
    var html = '';
    for (var i = 0; i < USERNAMES.length; i++) {
      var name = USERNAMES[i];
      html += '<option>' + name +'</option>';
    }
    return html;
  },
  handleSubmission: function() {
    // TODO check that there is at least two
    this.isRanked = $('#ranked-checkbox').is(':checked');
    var playerNames = $('#select-players').val();
    for (var i = 0; i < playerNames.length; i++) {
      var player = new Player(playerNames[i]);
      this.addPlayer(player);
    }
    this.showNextPlayerPage();
  },
  listenForSubmission: function(player) {
    var _this = this;
    $('#player-submit').click(function() {
      if (_this.playerIndex == _this.players.length) {
        _this.addGameToDatastore();
      }
      else {
        _this.showNextPlayerPage();
      }
    });
  },
  prepareRequest: function() {
    var playerData = [];
    for (var i = 0; i < this.players.length; i++) {
      var player = this.players[i];
      var data = player.buildRequestData();
      if (data === null) {
        // TODO
        console.error('Show some feedback');
        return;
      }
      playerData.push(data);
    }

    return {
      game_type: this.gameType,
      is_ranked: this.isRanked,
      players: playerData,
    };
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
    var player = this.players[this.playerIndex];
    var html = player.getHTML();
    this.div.html(html);
    this.listenForSubmission(player);
    this.playerIndex ++;
  },
  showSuccessfulPage: function() {
    this.div.html(
      '<h4>Congratulations! You\'re game was succesfully submitted!</h4>' +
      '<a href="/"><button class="btn btn-primary">Add Another Game</button></a>'
    );
  }
};
