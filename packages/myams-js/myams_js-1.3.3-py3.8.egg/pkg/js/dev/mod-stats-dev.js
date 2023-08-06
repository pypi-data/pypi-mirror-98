(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports);
    global.modStats = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.stats = void 0;

  /* global MyAMS */

  /**
   * MyAMS stats management
   */
  var $ = MyAMS.$;
  var stats = {
    logPageview: function logPageview() {},
    logEvent: function logEvent() {}
  };
  /**
   * Global module initialization
   */

  _exports.stats = stats;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('stats');
    } else {
      MyAMS.stats = stats;
      console.debug("MyAMS: stats module loaded...");
    }
  }
});
//# sourceMappingURL=mod-stats-dev.js.map
