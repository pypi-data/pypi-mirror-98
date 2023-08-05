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
    global.modContainer = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.container = void 0;

  /* global MyAMS */

  /**
   * MyAMS container management
   */
  var $ = MyAMS.$;
  var container = {
    deleteElement: function deleteElement(action) {
      return function (link, params) {
        MyAMS.require('ajax', 'alert', 'i18n').then(function () {
          MyAMS.alert.bigBox({
            status: 'danger',
            icon: 'fas fa-bell',
            title: MyAMS.i18n.WARNING,
            message: MyAMS.i18n.CONFIRM_REMOVE,
            successLabel: MyAMS.i18n.CONFIRM,
            cancelLabel: MyAMS.i18n.BTN_CANCEL
          }).then(function (status) {
            if (status !== 'success') {
              return;
            }

            var row = link.parents('tr'),
                table = row.parents('table');
            var location = link.data('ams-location') || row.data('ams-location') || table.data('ams-location') || '';

            if (location) {
              location += '/';
            }

            var deleteTarget = link.data('ams-delete-target') || row.data('ams-delete-target') || table.data('ams-delete-target') || 'delete-element.json',
                objectName = row.data('ams-element-name');
            MyAMS.ajax.post(location + deleteTarget, {
              'object_name': objectName
            }).then(function (result, status, xhr) {
              if (result.status === 'success') {
                if (table.hasClass('datatable')) {
                  table.DataTable().row(row).remove().draw();
                } else {
                  row.remove();
                }

                if (result.handle_json) {
                  MyAMS.ajax.handleJSON(result);
                }
              } else {
                MyAMS.ajax.handleJSON(result);
              }
            });
          });
        });
      };
    }
  };
  /**
   * Global module initialization
   */

  _exports.container = container;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('container');
    } else {
      MyAMS.container = container;
      console.debug("MyAMS: container module loaded...");
    }
  }
});
//# sourceMappingURL=mod-container-dev.js.map
