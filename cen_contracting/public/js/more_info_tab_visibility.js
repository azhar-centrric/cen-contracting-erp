// Previously the "More Info" tab was hidden for everyone via a blanket Property Setter.
// The client only wants it hidden for specific users (e.g. sales staff who don't need the
// Accounting/Commission fields in there), so visibility is now driven per-user from
// More Info Tab Settings instead, applied on every form refresh.
(function () {
	// The "More Info" tab's fieldname isn't consistent across doctypes - Quotation and Sales
	// Invoice both call it more_info_tab, Sales Order calls the same tab more_info.
	const TAB_FIELDNAME_BY_DOCTYPE = {
		Quotation: "more_info_tab",
		"Sales Invoice": "more_info_tab",
		"Sales Order": "more_info",
	};
	const SETTINGS_DOCTYPE = "More Info Tab Settings";

	async function apply_more_info_tab_visibility(frm) {
		// The tab button itself (the row of tab buttons at the top of the form) is a separate Tab
		// object in frm.layout.tabs, with its own df - toggle_display() only mutates the df on the
		// field Control in frm.fields_dict, which Tab.refresh() never reads, so the button stayed
		// visible even once the tab's content correctly went empty. Set the Tab's own df.hidden
		// directly instead.
		const tab_fieldname = TAB_FIELDNAME_BY_DOCTYPE[frm.doctype];
		const tab = frm.layout.tabs?.find((t) => t.df.fieldname === tab_fieldname);
		if (!tab) return;

		await frappe.model.with_doc(SETTINGS_DOCTYPE, SETTINGS_DOCTYPE);
		const settings = frappe.get_doc(SETTINGS_DOCTYPE, SETTINGS_DOCTYPE);
		const should_hide = (settings.hidden_for_users || []).some(
			(row) => row.user === frappe.session.user
		);

		tab.df.hidden = should_hide ? 1 : 0;
		frm.layout.refresh_tabs();
	}

	for (const doctype of Object.keys(TAB_FIELDNAME_BY_DOCTYPE)) {
		frappe.ui.form.on(doctype, {
			async refresh(frm) {
				await apply_more_info_tab_visibility(frm);
			},
		});
	}
})();
