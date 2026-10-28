import frappe


def execute():
	# "More Info" tab hiding on Quotation/Sales Invoice is now per-user (More Info Tab Settings +
	# public/js/more_info_tab_visibility.js) instead of hidden for everyone via these Property
	# Setters - the Quotation one came from set_quotation_properties(), the Sales Invoice one was
	# set directly via Customize Form and was never in code.
	for name in ("Quotation-more_info_tab-hidden", "Sales Invoice-more_info_tab-hidden"):
		if frappe.db.exists("Property Setter", name):
			frappe.delete_doc("Property Setter", name, ignore_permissions=True)

	frappe.clear_cache(doctype="Quotation")
	frappe.clear_cache(doctype="Sales Invoice")
