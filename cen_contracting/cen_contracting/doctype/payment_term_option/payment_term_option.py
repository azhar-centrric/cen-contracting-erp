# Copyright (c) 2026, Centrric Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PaymentTermOption(Document):
	def validate(self):
		if self.is_default and self.disabled:
			frappe.throw(_("The default Payment Term can't be disabled"))

	def on_update(self):
		# Only one default: ticking it here clears it from the others
		if self.is_default:
			frappe.db.set_value(
				"Payment Term Option", {"is_default": 1, "name": ["!=", self.name]}, "is_default", 0
			)


@frappe.whitelist()
def get_payment_term_options(txt=None, **kwargs):
	# Suggestions for the cen_payment_terms Autocomplete field; anyone who can edit a
	# Quotation/Sales Order/Sales Invoice may see the list, so read it without permission checks.
	filters = {"disabled": 0}
	if txt:
		filters["payment_term"] = ["like", f"%{txt}%"]
	return frappe.get_all(
		"Payment Term Option", filters=filters, pluck="payment_term", order_by="is_default desc, payment_term asc"
	)


@frappe.whitelist()
def get_default_payment_term():
	return frappe.db.get_value("Payment Term Option", {"is_default": 1, "disabled": 0}, "payment_term")
