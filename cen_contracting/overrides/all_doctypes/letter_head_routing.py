import frappe


def set_dynamic_letter_head(doc, method=None):
	if not doc.meta.has_field("letter_head"):
		return

	# Runs on every insert site-wide, so read the cached single rather than hitting the DB.
	mapped = next(
		(
			row.default_letter_head
			for row in frappe.get_cached_doc("Print Routing Settings").mappings
			if row.document_type == doc.doctype
		),
		None,
	)
	if not mapped:
		return

	# New documents arrive pre-filled with the default Letter Head (the global default, or the
	# Company's default via ERPNext's form), so those don't count as a manual selection.
	if doc.letter_head and doc.letter_head not in get_auto_filled_letter_heads(doc):
		return

	doc.letter_head = mapped


def get_auto_filled_letter_heads(doc):
	letter_heads = {frappe.db.get_default("letter_head")}
	if doc.get("company"):
		letter_heads.add(frappe.get_cached_value("Company", doc.company, "default_letter_head"))

	# "Make From" flows (e.g. Sales Order -> Sales Invoice) copy the source document's
	# letter_head onto the new one before this hook runs - that's inheritance, not a deliberate
	# choice, so any OTHER doctype's routed letter head should still count as auto-filled too.
	for row in frappe.get_cached_doc("Print Routing Settings").mappings:
		if row.document_type != doc.doctype:
			letter_heads.add(row.default_letter_head)

	return letter_heads


def backfill_letter_head_routing():
	"""One-time (idempotent) fix for documents that predate this hook - e.g. the Tally-migrated
	Quotations/Sales Invoices, which were bulk-inserted and never went through before_insert."""
	settings = frappe.get_cached_doc("Print Routing Settings")

	for row in settings.mappings:
		if not row.default_letter_head:
			continue

		meta = frappe.get_meta(row.document_type)
		if not meta.has_field("letter_head"):
			continue

		fields = ["name", "letter_head"]
		if meta.has_field("company"):
			fields.append("company")

		candidates = frappe.get_all(
			row.document_type,
			filters={"letter_head": ["!=", row.default_letter_head]},
			fields=fields,
		)
		for candidate in candidates:
			candidate.doctype = row.document_type
			if candidate.letter_head and candidate.letter_head not in get_auto_filled_letter_heads(candidate):
				continue  # genuinely manually chosen - leave it alone
			frappe.db.set_value(row.document_type, candidate.name, "letter_head", row.default_letter_head)
