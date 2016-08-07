function Game(gameDiv) {
  this.div = gameDiv;
  this.gameType = null;
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
      error: function(data) {
        var m = 'Could not save game data: ' + data.responseText;
        feedback.alert(m, 'red');
      }
    });
  },
  addPlayer: function(playerName) {
    this.players.push(playerName);
  },
  createInitialView: function() {
    this.div.html(this.getInitialViewHTML());
    var gameSelectDiv = $('#game-select');
    gameSelectDiv.select2({
      placeholder: 'Select a game'
    });
    this.listenForGameTypeSelection();
  },
  getPaginationHTML: function() {
    $('#paginator').remove();
    var playerHTML = '';
    for (var i = 0; i < this.players.length; i++) {
      var active = '';
      if (this.playerIndex == i) {
        active = ' class="active"';
      }
      playerHTML += '<li' + active + '><a href="#">' + (i + 1) + '</a></li>';
    }
    return '<div id="paginator"><ul class="pagination">' + playerHTML + '</ul></div>';
  },
  enableGameSelect: function() {
    this.div.find('#game-select').prop('disabled', false);
  },
  isValidPage: function(pageNum) {
    return pageNum > 0 && pageNum <= this.players.length;
  },
  goToPage: function(pageNum, saveCurrentPlayer) {
    if (saveCurrentPlayer || saveCurrentPlayer === undefined) {
      this.saveCurrentPlayer();
    }

    if (!this.isValidPage(pageNum)) {
      return;
    }

    this.playerIndex = pageNum - 1;
    var player = this.players[this.playerIndex];

    var playerHTML = player.getHTML();
    this.div.html(playerHTML);

    var paginationHTML = this.getPaginationHTML();
    this.div.find('#user-input').append(paginationHTML);

    this.listenForPageChange();
    this.listenForSubmission(player);
  },
  getInitialViewHTML: function() {
    var html =
    '<div class="row">' +
      '<div class="col-md-12 col-sm-12">' +
        '<h4>Create a new game</h4>' +
      '</div>' +
    '</div>' +
    '<div class="row">' +
      '<div class="col-md-4 col-sm-4">' +
        '<select class="form-control" id="game-select" disabled>' +
          '<option></option>' +
          '<option>' +
            'Pool - Cut throat' +
          '</option>' +
          '<option>' +
            'Pool - Eight ball' +
          '</option>' +
        '</select>' +
      '</div>' +
    '</div>' +
    '<div class="row">' +
      '<div id="options" class="col-md-4 col-sm-4"></div>' +
    '</div>';
    return html;
  },
  getNextPageNumber: function() {
    var currentPage = this.playerIndex + 1;
    var nextPage = currentPage + 1;
    return nextPage;
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
  setUpPlayerInput: function() {
    feedback.clear();
    this.isRanked = $('#ranked-checkbox').is(':checked');
    var playerNames = $('#select-players').val();

    if (playerNames.length < 2) {
      feedback.alert('You can\'t play by yourself!', 'red');
      return;
    }

    for (var i = 0; i < playerNames.length; i++) {
      var player = new Player(playerNames[i]);
      this.addPlayer(player);
    }
    this.goToPage(1, false);
  },
  listenForGameTypeSelection: function() {
    var _this = this;
    $('#game-select').on('change', function() {
      var select = $(this);
      var gameType = select.val();
      _this.updateGameType(gameType);
    });
  },
  listenForPageChange: function() {
    var _this = this;
    $('#paginator ul li').click(function() {
      var li = $(this);
      if (li.hasClass('active')) {
        return;
      }
      var pageNum = parseInt($(this).text());
      _this.goToPage(pageNum);
    });
  },
  listenForSubmission: function(player) {
    var _this = this;
    $('#player-submit').click(function() {
      var nextPage = _this.getNextPageNumber();
      if (_this.isValidPage(nextPage)) {
        _this.goToPage(nextPage);
      }
      else {
        _this.saveCurrentPlayer();
        _this.addGameToDatastore();
      }
    });
  },
  playersToPayload: function() {
    var playerData = [];
    for (var i = 0; i < this.players.length; i++) {
      var player = this.players[i];
      var data = player.toDict();
      playerData.push(data);
    }
    return playerData;
  },
  prepareRequest: function() {
    return {
      game_type: this.gameType,
      is_ranked: this.isRanked,
      players: this.playersToPayload(),
    };
  },
  saveCurrentPlayer: function() {
    var currentPlayer = this.players[this.playerIndex];
    currentPlayer.save();
  },
  setUpSubmissonHandler: function() {
    var _this = this;
    $('#submit-game').click(function() {
      _this.setUpPlayerInput();
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
  showSuccessfulPage: function() {
    this.div.html(
      '<h4>Congratulations! You\'re game was succesfully submitted!</h4>' +
      '<a href="/"><button class="btn btn-primary">Add Another Game</button></a>'
    );
  },
  updateGameType: function(gameType) {
    game.gameType = gameType;
    game.showOptions();
    game.setUpSubmissonHandler();
  }
};
