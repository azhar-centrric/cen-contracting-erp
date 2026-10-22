import frappe

# The primary mechanism for this feature is client-side (public/js/default_terms_and_conditions.js)
# - the Desk "+ New" form never talks to the server until Save, so onload() never actually fires for
# it. This server-side onload hook is a defensive fallback for document creation paths that DO
# involve a server round-trip (API-created drafts, Quick Entry, etc). ERPNext natively auto-fills
# tc_name from Company.default_selling_terms / default_buying_terms on these doctypes in that same
# situation (see SellingController/BuyingController.onload()); our mapping is more specific, so it
# should override that native default - but only the native default, never a value actually picked.
SELLING_DOCTYPES = {"Quotation", "Sales Order", "Sales Invoice", "Delivery Note", "POS Invoice"}
BUYING_DOCTYPES = {
	"Purchase Order",
	"Purchase Invoice",
	"Purchase Receipt",
	"Supplier Quotation",
	"Request for Quotation",
	"Material Request",
}

FIELD_BY_DOCTYPE = {
	**{dt: "tc_name" for dt in SELLING_DOCTYPES | BUYING_DOCTYPES},
	"Blanket Order": "tc_name",
	"Job Offer": "select_terms",
}


def apply_default_terms(doc, method=None):
	if not doc.is_new():
		return

	fieldname = FIELD_BY_DOCTYPE.get(doc.doctype)
	if not fieldname:
		return

	current_value = doc.get(fieldname)
	if current_value and current_value != get_native_default_terms(doc):
		return  # user-picked (or already applied by us on an earlier onload) - leave it alone

	mapped = next(
		(
			row.terms_and_conditions
			for row in frappe.get_cached_doc("Default Terms and Conditions Settings").mapping
			if row.document_type == doc.doctype and row.company == doc.get("company")
		),
		None,
	)
	if not mapped or mapped == current_value:
		return

	doc.set(fieldname, mapped)
	terms_text = frappe.get_cached_value("Terms and Conditions", mapped, "terms")
	if terms_text:
		doc.set("terms", terms_text)


def get_native_default_terms(doc):
	if not doc.get("company"):
		return None
	if doc.doctype in SELLING_DOCTYPES:
		return frappe.get_cached_value("Company", doc.company, "default_selling_terms")
	if doc.doctype in BUYING_DOCTYPES:
		return frappe.get_cached_value("Company", doc.company, "default_buying_terms")
	return None
