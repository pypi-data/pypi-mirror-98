/* global MyAMS */
/**
 * MyAMS container management
 */

const $ = MyAMS.$;


export const container = {

	deleteElement: (action) => {
		return function(link, params) {
			MyAMS.require('ajax', 'alert', 'i18n').then(() => {
				MyAMS.alert.bigBox({
					status: 'danger',
					icon: 'fas fa-bell',
					title: MyAMS.i18n.WARNING,
					message: MyAMS.i18n.CONFIRM_REMOVE,
					successLabel: MyAMS.i18n.CONFIRM,
					cancelLabel: MyAMS.i18n.BTN_CANCEL
				}).then((status) => {
					if (status !== 'success') {
						return;
					}
					const
						row = link.parents('tr'),
						table = row.parents('table');
					let location = link.data('ams-location') || row.data('ams-location') || table.data('ams-location') || '';
					if (location) {
						location += '/';
					}
					const
						deleteTarget = link.data('ams-delete-target') || row.data('ams-delete-target') ||
							table.data('ams-delete-target') || 'delete-element.json',
						objectName = row.data('ams-element-name');
					MyAMS.ajax.post(location + deleteTarget, {
						'object_name': objectName
					}).then((result, status, xhr) => {
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
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('container');
	} else {
		MyAMS.container = container;
		console.debug("MyAMS: container module loaded...");
	}
}
