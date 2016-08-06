function Player(playerName) {
  this.name = playerName;
}

Player.prototype = {
  constructor: Player,

  getHTML: function() {
    var html =
      '<h4>' + this.name + '</h4>'+
      '<div class="col-md-2 col-sm-2">' +
        '<div class="form-group">' +
          '<label>Placement</label>' +
          '<input id="placement" class="form-control" type="number">' +
        '</div>' +
        '<div class="form-group">' +
          '<label>Number of balls hit in</label>' +
          '<input id="num-hit-in" class="form-control" type="number">' +
        '</div>' +
        '<div class="form-group">' +
          '<label>Number of balls left</label>' +
          '<input id="num-left" class="form-control" type="number">' +
        '</div>' +
        '<div class="form-group">' +
          '<label>Number of scratches</label>' +
          '<input id="num-scratches" class="form-control" type="number">' +
        '</div>' +
        '<div class="form-group">' +
          '<label>Lag rank</label>' +
          '<input id="lag-rank" class="form-control" type="number">' +
        '</div>' +
        '<button id="player-submit" class="btn btn-primary">Submit</button>' +
      '</div>';
    return html;
  },

  getInputData: function() {
    return {
      balls_hit_in: $('#num-hit-in').val(),
      balls_remaining: $('#num-left').val(),
      lag_rank: $('#lag-rank').val(),
      player_placement: $('#placement').val(),
      scratch_count: $('#num-scratches').val(),
    };
  },

  handleSubmission: function() {
    console.log('Validate data');
    var inputData = this.getInputData();
    if (this.isValidData(inputData)) {
      console.log('Send data');
    }
    else {
      console.log('Show error');
    }
  },

  isValidData: function(inputData) {
    for (var playerAttribute in inputData) {
      if (inputData.hasOwnProperty(playerAttribute)) {
        var number = this.parseNumber(inputData[playerAttribute]);
        if (number < 0) {
          return false;
        }
      }
    }
    return true;
  },

  parseNumber: function(number) {
    if (number === "") {
      number = 0;
    }
    else {
      number = parseInt(number);
    }
    return number;
  },

  setUpSubmissonHandler: function() {
    var _this = this;
    $('#player-submit').click(function() {
      _this.handleSubmission();
    });
  }
};
