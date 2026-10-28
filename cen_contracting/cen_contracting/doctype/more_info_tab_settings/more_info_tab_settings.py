# Copyright (c) 2026, Centrric Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class MoreInfoTabSettings(Document):
	def validate(self):
		self.validate_duplicate_users()

	def validate_duplicate_users(self):
		seen = set()
		for row in self.hidden_for_users:
			if row.user in seen:
				frappe.throw(_("Row {0}: {1} is already in this list").format(row.idx, row.user))
			seen.add(row.user)
