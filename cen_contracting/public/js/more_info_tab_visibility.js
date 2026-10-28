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
	}

	for (const doctype of DOCTYPES) {
		frappe.ui.form.on(doctype, {
			async refresh(frm) {
				await apply_more_info_tab_visibility(frm);
			},
		});
	}
})();
