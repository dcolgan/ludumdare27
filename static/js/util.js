// Generated by CoffeeScript 1.6.3
var Util;

Util = (function() {
  function Util() {}

  Util.calculate_distance = function(x1, y1, x2, y2) {
    return Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
  };

  Util.random_choice = function(collection) {
    return collection[Math.floor(Math.random() * collection.length)];
  };

  return Util;

})();