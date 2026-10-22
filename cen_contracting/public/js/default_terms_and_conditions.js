// ERPNext's native "default_selling_terms"/"default_buying_terms" fill (and our own override) both
// run entirely client-side, triggered off the "company" field-change event (erpnext/public/js/
// controllers/transaction.js -> company() -> set_terms()), reading cached Company boot data - there
// is no server round-trip when a brand-new document is opened, so a server-side onload hook never
// fires here. This registers the same kind of "company" trigger, using a per-doctype mapping from
// Default Terms and Conditions Settings instead of one blanket value per Selling/Buying module.
// Because frappe.ui.form's new-style handlers (this one) always run before the doctype's own
// old-style class methods for the same event (see script_manager.js get_handlers/trigger), and this
// handler is async, ERPNext's own set_terms() genuinely waits for this to finish first - so once we
// set a value here, its own "if (!tc_name)" guard correctly leaves it alone.
(function () {
	const FIELD_BY_DOCTYPE = {
		Quotation: "tc_name",
		"Sales Order": "tc_name",
		"Sales Invoice": "tc_name",
		"Delivery Note": "tc_name",
		"POS Invoice": "tc_name",
		"Purchase Order": "tc_name",
		"Purchase Invoice": "tc_name",
		"Purchase Receipt": "tc_name",
		"Supplier Quotation": "tc_name",
		"Request for Quotation": "tc_name",
		"Material Request": "tc_name",
		"Blanket Order": "tc_name",
		"Job Offer": "select_terms",
	};

	async function apply_mapped_terms(frm) {
		if (!frm.is_new() || !frm.doc.company) return;

		const fieldname = FIELD_BY_DOCTYPE[frm.doc.doctype];
		if (!fieldname || frm.doc[fieldname]) return;

		await frappe.model.with_doc(
			"Default Terms and Conditions Settings",
			"Default Terms and Conditions Settings"
		);
		const settings = frappe.get_doc(
			"Default Terms and Conditions Settings",
			"Default Terms and Conditions Settings"
		);
		const row = (settings.mapping || []).find(
			(r) => r.document_type === frm.doc.doctype && r.company === frm.doc.company
		);
		if (!row || !row.terms_and_conditions || frm.doc[fieldname] === row.terms_and_conditions) return;

		await frm.set_value(fieldname, row.terms_and_conditions);
	}

	for (const doctype of Object.keys(FIELD_BY_DOCTYPE)) {
		frappe.ui.form.on(doctype, {
			async company(frm) {
				await apply_mapped_terms(frm);
			},
			async refresh(frm) {
				await apply_mapped_terms(frm);
			},
		});
	}
})();
