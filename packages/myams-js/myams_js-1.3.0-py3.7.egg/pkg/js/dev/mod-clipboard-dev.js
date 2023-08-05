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
    global.modClipboard = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.clipboard = void 0;

  /* global MyAMS, clipboardData */

  /**
   * MyAMS i18n translations
   */
  var $ = MyAMS.$;
  /**
   * Internal function used to copy text to clipboard
   *
   * @param text: text to be copied
   */

  function doCopy(text) {
    var copied = false;

    if (window.clipboardData && window.clipboardData.setData) {
      // IE specific code
      copied = clipboardData.setData("Text", text);
    } else if (document.queryCommandSupported && document.queryCommandSupported('copy')) {
      var textarea = $('<textarea>');
      textarea.val(text).css('position', 'fixed') // prevent scrolling to bottom of page in Edge
      .appendTo(MyAMS.dom.root);
      textarea.get(0).select();

      try {
        document.execCommand('copy'); // security exception may be thrown by some browsers!

        copied = true;
      } catch (e) {
        console.warn("Clipboard copy failed!", e);
      } finally {
        textarea.remove();
      }
    }

    if (copied) {
      MyAMS.require('i18n', 'alert').then(function () {
        MyAMS.alert.smallBox({
          status: 'success',
          message: text.length > 1 ? MyAMS.i18n.CLIPBOARD_TEXT_COPY_OK : MyAMS.i18n.CLIPBOARD_CHARACTER_COPY_OK,
          icon: 'fa-info-circle',
          timeout: 3000
        });
      });
    } else {
      MyAMS.require('i18n').then(function () {
        prompt(MyAMS.i18n.CLIPBOARD_COPY, text);
      });
    }
  }

  var clipboard = {
    /**
     * Copy given text to system's clipboard
     *
     * @param text: text to be copied
     */
    copy: function copy(text) {
      if (typeof text === 'undefined') {
        return function () {
          var source = $(this),
              text = source.text();
          source.parents('.btn-group').removeClass('open');
          doCopy(text);
        };
      } else {
        doCopy(text);
      }
    }
  };
  /**
   * Global module initialization
   */

  _exports.clipboard = clipboard;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('clipboard');
    } else {
      MyAMS.clipboard = clipboard;
      console.debug("MyAMS: clipboard module loaded...");
    }
  }
});
//# sourceMappingURL=mod-clipboard-dev.js.map
