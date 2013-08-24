// Generated by CoffeeScript 1.6.3
var GAME;

GAME = {
  home: function() {},
  create_accout: function() {},
  game: function() {
    var gameViewModel;
    gameViewModel = function() {
      var vm;
      vm = this;
      vm.actions = {
        walk: {
          name: 'Walk',
          seconds: 1,
          stamina: 0
        },
        run: {
          name: 'Run',
          seconds: 1,
          stamina: 2
        },
        left: {
          name: 'Turn Left',
          seconds: 1,
          stamina: 0
        },
        right: {
          name: 'Turn Right',
          seconds: 1,
          stamina: 0
        },
        reverse: {
          name: 'Turn Around',
          seconds: 1,
          stamina: 0
        }
      };
      vm.secondsRemaining = ko.observable(10);
      vm.chosenActions = ko.observableArray([]);
      vm.chooseAction = function(data, event) {
        var thisAction;
        thisAction = vm.actions[$(event.target).data('action')];
        if (vm.secondsRemaining() - thisAction.seconds >= 0) {
          vm.secondsRemaining(vm.secondsRemaining() - thisAction.seconds);
          return vm.chosenActions.push(thisAction);
        }
      };
      vm.cancelAction = function(data, event) {
        debugger;
      };
      return null;
    };
    return ko.applyBindings(new gameViewModel)({
      updateSecondsRemainingDisplay: function() {
        return $('#seconds-left').text(this.secondsRemaining);
      },
      chooseAction: function(which) {
        var $newActionButton;
        $newActionButton = $(actionButtonTemplate);
        $newActionButton.text($(this).data('action'));
        $newAction.text();
        $newAction.click(function() {
          return $(this).remove();
        });
        $newAction.hover((function() {
          $(this).removeClass('btn-success');
          return $(this).addClass('btn-danger');
        }), (function() {
          $(this).addClass('btn-success');
          return $(this).removeClass('btn-danger');
        }));
        return $('.actions-panel').append($newAction);
      }
    });
  }
};

$(function() {
  var cl;
  $.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
        return xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
      }
    }
  });
  cl = $('body').attr('class');
  if (cl) {
    return GAME[cl]();
  }
});