function Player(playerName) {
  this.name = playerName;

  this.balls_hit_in = null;
  this.balls_remaining = null;
  this.lag_rank = null;
  this.player_placement = null;
  this.scratch_count = null;
}

Player.prototype = {
  constructor: Player,

  getHTML: function(buttonText) {
    if (!buttonText) {
      buttonText = "Next";
    }
    var dict = this.toHTMLDict();
    var html =
      '<h4>' + this.name + '</h4>'+
      '<div id="user-input" class="col-md-2 col-sm-2">' +
        '<div class="form-group">' +
          '<label>Placement</label>' +
          '<input id="placement" class="form-control" type="number"' + dict.player_placement + '>' +
        '</div>' +
        '<div class="form-group">' +
          '<label>Number of balls hit in</label>' +
          '<input id="num-hit-in" class="form-control" type="number"' + dict.balls_hit_in + '>' +
        '</div>' +
        '<div class="form-group">' +
          '<label>Number of balls left</label>' +
          '<input id="num-left" class="form-control" type="number"' + dict.balls_remaining + '>' +
        '</div>' +
        '<div class="form-group">' +
          '<label>Number of scratches</label>' +
          '<input id="num-scratches" class="form-control" type="number"' + dict.scratch_count + '>' +
        '</div>' +
        '<div class="form-group">' +
          '<label>Lag rank</label>' +
          '<input id="lag-rank" class="form-control" type="number"' + dict.lag_rank + '>' +
        '</div>' +
        '<div><button id="player-submit" class="btn btn-primary">' + buttonText +'</button></div>' +
      '</div>';
    return html;
  },
  parseInputs: function() {
    return {
      balls_hit_in: $('#num-hit-in').val(),
      balls_remaining: $('#num-left').val(),
      lag_rank: $('#lag-rank').val(),
      player_placement: $('#placement').val(),
      scratch_count: $('#num-scratches').val(),
    };
  },

  toDict: function() {
    var dictionary = {};
    for (var attribute in this) {
      if (this.hasOwnProperty(attribute)) {
        var value = this[attribute];
        if (value === null) {
          value = this.getDefaultValue(attribute);
        }
        dictionary[attribute] = value;
      }
    }
    return dictionary;
  },

  getDefaultValue: function(attribute) {
    if (['lag_rank', 'player_placement'].indexOf(attribute) >= 0) {
      return 1;
    }
    return 0;
  },

  toHTMLDict: function() {
    return {
      balls_hit_in: this.balls_hit_in === null ? '' : ' value="' + this.balls_hit_in + '"',
      balls_remaining: this.balls_remaining === null ? '' : ' value="' + this.balls_remaining + '"',
      lag_rank: this.lag_rank === null ? '' : ' value="' + this.lag_rank + '"',
      player_placement: this.player_placement === null ? '' : ' value="' + this.player_placement + '"',
      scratch_count: this.scratch_count === null ? '' : ' value="' + this.scratch_count + '"',
    };
  },

  save: function() {
    var html = this.getHTML();
    var data = this.parseInputs();
    for (var attribute in data) {
      if (data.hasOwnProperty(attribute)) {
        var value = data[attribute];
        if (this.isValidProperty(attribute, value)) {
          this[attribute] = parseInt(value);
        }
      }
    }
  },

  isValidProperty: function(attribute, value) {
    if (value === null || value === "") {
      return false;
    }
    if (value < 0) {
      return false;
    }
    if (attribute == "lag_rank" && value < 1) {
      return false;
    }
    if (attribute == "player_placement" && value < 1) {
      return false;
    }
    return true;
  },
};
