// Previously the "More Info" tab was hidden for everyone via a blanket Property Setter.
// The client only wants it hidden for specific users (e.g. sales staff who don't need the
// Accounting/Commission fields in there), so visibility is now driven per-user from
// More Info Tab Settings instead, applied on every form refresh.
(function () {
	const DOCTYPES = ["Quotation", "Sales Invoice"];
	const SETTINGS_DOCTYPE = "More Info Tab Settings";

	async function apply_more_info_tab_visibility(frm) {
		if (!frm.fields_dict.more_info_tab) return;

		await frappe.model.with_doc(SETTINGS_DOCTYPE, SETTINGS_DOCTYPE);
		const settings = frappe.get_doc(SETTINGS_DOCTYPE, SETTINGS_DOCTYPE);
		const should_hide = (settings.hidden_for_users || []).some(
			(row) => row.user === frappe.session.user
		);

		frm.toggle_display("more_info_tab", !should_hide);

		// toggle_display only flips the field's hidden flag - the tab strip itself (the row of tab
		// buttons at the top of the form) only re-reads that flag inside refresh_tabs(), which isn't
		// triggered on its own since this field has no depends_on driving the normal dependency
		// refresh cycle. Without this call the tab button stays visible even though its content
		// (correctly) becomes empty.
		frm.layout.refresh_tabs();
	}

	for (const doctype of DOCTYPES) {
		frappe.ui.form.on(doctype, {
			async refresh(frm) {
				await apply_more_info_tab_visibility(frm);
			},
		});
	}
})();
