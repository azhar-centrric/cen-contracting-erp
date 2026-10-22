import frappe

# Frappe quirk: the moment ANY Custom DocPerm row exists for a doctype (at any permlevel, for any
# role), frappe.permissions.get_valid_perms() stops consulting that doctype's standard (hardcoded)
# DocPerm rows entirely - for every OTHER role, site-wide. Our role setup scripts
# (admin.py/accountant.py/supervisor.py) grant Classy Admin/Accountant/Project Supervisor access to
# many shared doctypes (e.g. Address, Quotation, Item) via Custom DocPerm - which silently strips
# every other role's original access to those same doctypes unless it's explicitly replicated here.
# This restores the original standard permissions as explicit Custom DocPerm rows for every role
# that would otherwise have lost them, so nothing site-wide regresses as a side effect of our own
# role grants. Idempotent and safe to re-run on every migrate - also self-heals if a future role
# script introduces the same problem on a new doctype.

PERM_FLAGS = [
	"if_owner",
	"read",
	"write",
	"create",
	"delete",
	"submit",
	"cancel",
	"amend",
	"report",
	"export",
	"import",
	"share",
	"print",
	"email",
	"select",
	"mask",
]


def restore_suppressed_standard_permissions():
	doctypes_with_custom_perms = frappe.get_all("Custom DocPerm", pluck="parent", distinct=True)

	for doctype in doctypes_with_custom_perms:
		if not frappe.db.exists("DocType", doctype):
			continue

		standard_rows = frappe.get_all(
			"DocPerm", filters={"parent": doctype}, fields=["role", "permlevel", *PERM_FLAGS]
		)
		custom_role_levels = {
			(r.role, r.permlevel)
			for r in frappe.get_all("Custom DocPerm", filters={"parent": doctype}, fields=["role", "permlevel"])
		}

		for row in standard_rows:
			key = (row.role, row.permlevel)
			if key in custom_role_levels:
				continue  # this role already has an explicit Custom DocPerm - leave it as-is

			docperm = frappe.new_doc("Custom DocPerm")
			docperm.parent = doctype
			docperm.parenttype = "DocType"
			docperm.parentfield = "permissions"
			docperm.role = row.role
			docperm.permlevel = row.permlevel
			for flag in PERM_FLAGS:
				docperm.set(flag, row.get(flag))
			docperm.insert(ignore_permissions=True)
			custom_role_levels.add(key)

	frappe.clear_cache()
