// ERPNext's own transaction controller (erpnext/public/js/controllers/transaction.js -> refresh())
// unconditionally force-shows the "naming_series" field on every new document, overriding any
// "hidden" Property Setter. For these doctypes a Document Naming Rule silently overrides whatever
// series the field shows, so it's actively misleading - wrap the shared function so it keeps the
// field hidden specifically here, and leaves every other doctype's native behaviour untouched.
(function () {
	const DOCTYPES_WITH_HIDDEN_SERIES = [
		"Quotation",
		"Sales Order",
		"Sales Invoice",
		"Purchase Order",
		"Purchase Invoice",
		"Purchase Receipt",
		"Supplier Quotation",
	];

	function patch() {
		if (!window.erpnext || typeof erpnext.toggle_naming_series !== "function") return false;
		if (erpnext.toggle_naming_series.__cen_patched) return true;

		const original_toggle_naming_series = erpnext.toggle_naming_series;

		const patched = function () {
			if (cur_frm && DOCTYPES_WITH_HIDDEN_SERIES.includes(cur_frm.doctype)) {
				cur_frm.toggle_display("naming_series", false);
				return;
			}
			return original_toggle_naming_series.apply(this, arguments);
		};
		patched.__cen_patched = true;
		erpnext.toggle_naming_series = patched;
		return true;
	}

	// Script tag order already guarantees erpnext.bundle.js has run before this file, but
	// retry briefly as a defensive fallback in case that ordering is ever disturbed.
	if (!patch()) {
		let attempts = 0;
		const interval = setInterval(() => {
			attempts += 1;
			if (patch() || attempts > 20) clearInterval(interval);
		}, 100);
	}
})();
