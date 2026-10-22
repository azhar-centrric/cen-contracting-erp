# Copyright (c) 2026, Centrric Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class DefaultTermsandConditionsSettings(Document):
	def validate(self):
		self.validate_duplicate_mappings()

	def validate_duplicate_mappings(self):
		seen = set()
		for row in self.mapping:
			key = (row.document_type, row.company)
			if key in seen:
				frappe.throw(
					_("Row {0}: Duplicate mapping for {1} + {2}").format(
						row.idx, row.document_type, row.company
					)
				)
			seen.add(key)
