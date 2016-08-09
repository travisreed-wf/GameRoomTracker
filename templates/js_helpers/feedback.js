/*
Taken from w-rmconsole app
*/

function Feedback(div) {
  /**
   * Initializes a Feedback Class that can be used to send messages to the user.
   *
   * Requires a div in the HTML:
   *   ``` HTML
   *   <div class="feedback" style="display: none"></div>
   *   ```
   *
   * The class can then be initialized in the JS by calling
   *   ``` javascript
   *   var div = $('.feedback');
   *   var feedback = new Feedback(div);
   *   ```
   */

  this.div = div;
}

/******************
Class-type Methods
*******************/
Feedback.prototype = {
  constructor: Feedback,

  alert: function(message, color, fadeOut, clear) {
    /** Send message through Feedback
     * @param {String} message - text or html to display
     * @param {String} color - green, blue, yellow, or red
     * @param {Number} fadeOut - ms to show message
     * @param {Boolean} clear - true to remove previous alerts
     */

    switch (color) {
      case 'green': alertClass = 'success'; break;
      case 'yellow': alertClass = 'warning'; break;
      case 'red': alertClass = 'danger'; break;
      default:
        alertClass = 'info';
    }

    // Default to no fadeOut if not specified
    fadeOut = fadeOut || 0;

    // Clear previous messages
    if (clear) {
      this.clear();
    }

    // Create div
    var alert = '<div class="alert alert-dismissible alert-' + alertClass+ '">' +
      '<button type="button" class="close"><span>&times;</span></button>' +
      message + '</div>';
    alert = $($.parseHTML(alert));
    alert.find('a').addClass('alert-link');
    this.div.append(alert);
    this.div.show();

    // Listener for alert dismiss
    alert.find('button.close').click(function() {
      alert.remove();
    });

    // Fadeout alert
    var _this = this;
    if (fadeOut > 0) {
      setTimeout(function(){
        alert.fadeOut();
        var visibleAlerts = _this.div.find('.alert:visible');
        if (visibleAlerts.length === 0) {
          _this.div.hide();
        }
      }, fadeOut);
    }
  },

  // Clear the Feedback
  clear: function() { this.div.html(''); },

  // Hides the Feedback
  hide: function() { this.div.hide(); },

  // Shows the Feedback
  show: function() { this.div.show(); },

};
