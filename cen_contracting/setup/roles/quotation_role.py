import frappe


def setup_quotation_role():
    # "Quotation role" was created manually via the UI (Role Permission Manager), not in code -
    # against this app's own convention (DEVELOPER_GUIDE.md rule 5). Reviewed and found it was
    # missing several doctypes a user with only this role needs to actually read and complete the
    # Quotation creation process end to end - verified by simulating the full flow (insert, submit,
    # print, cancel) as a user with exactly this role and nothing else. This file now captures the
    # role's full permission set (the doctypes the user had already granted manually, plus the
    # missing ones below), so it's reproducible on every site this app installs on, not just this one.
    role_name = "Quotation role"

    if not frappe.db.exists("Role", role_name):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": 1,
        }).insert(ignore_permissions=True)

    perms = [
        # Already configured manually on this site - kept as-is.
        {"parent": "Customer", "read": 1, "export": 1},
        {"parent": "Customer Group", "read": 1, "export": 1},
        {"parent": "Default Terms and Conditions Settings", "read": 1, "export": 1},
        {"parent": "Item", "read": 1, "write": 1, "create": 1, "delete": 1, "report": 1, "export": 1, "print": 1, "email": 1, "share": 1},
        {"parent": "Quotation", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "report": 1, "export": 1, "print": 1, "email": 1, "share": 1},
        {"parent": "Sales Taxes and Charges Template", "read": 1, "export": 1},
        {"parent": "Tax Category", "read": 1, "export": 1},
        {"parent": "Terms and Conditions", "read": 1, "export": 1},
        {"parent": "Territory", "read": 1, "export": 1},

        # Missing - every Link field on Quotation (and its items/taxes child tables) is permission
        # checked independently the moment a value is set, even with full access to Quotation
        # itself. Without these, creating or saving a real Quotation throws PermissionError:
        #   - Price List: doc.selling_price_list
        #   - UOM: each Quotation Item row's uom/stock_uom
        #   - Company: doc.company (mandatory on every Quotation)
        #   - Project: cen_choose_project (existing project) and viewing one this role
        #     auto-creates (overrides/quotation/project_creation.py inserts it with
        #     ignore_permissions=True, so "create" isn't needed here, only "read")
        #   - Payment Term Option: backs the cen_payment_terms Autocomplete dropdown
        #   - Address / Contact: rendering the customer's address_display/contact_display in
        #     set_missing_values() - the base "All" role grant on both is if_owner-restricted
        #     (see tabDocPerm), so it only covers addresses/contacts this user personally
        #     created, not an existing customer's
        #   - Account: get_party_account() resolves the customer's receivable account while
        #     building the payment schedule, even though nothing about Account is shown on
        #     the Quotation form itself
        {"parent": "Price List", "read": 1},
        {"parent": "UOM", "read": 1},
        {"parent": "Company", "read": 1},
        {"parent": "Project", "read": 1},
        {"parent": "Payment Term Option", "read": 1},
        {"parent": "Address", "read": 1},
        {"parent": "Contact", "read": 1},
        {"parent": "Account", "read": 1},
    ]

    for p in perms:
        existing = frappe.db.exists("Custom DocPerm", {"parent": p["parent"], "role": role_name})
        docperm = frappe.get_doc("Custom DocPerm", existing) if existing else frappe.new_doc("Custom DocPerm")
        docperm.parent = p["parent"]
        docperm.parenttype = "DocType"
        docperm.parentfield = "permissions"
        docperm.role = role_name
        docperm.read = p.get("read", 0)
        docperm.write = p.get("write", 0)
        docperm.create = p.get("create", 0)
        docperm.delete = p.get("delete", 0)
        docperm.submit = p.get("submit", 0)
        docperm.cancel = p.get("cancel", 0)
        docperm.report = p.get("report", 0)
        docperm.export = p.get("export", 0)
        docperm.print = p.get("print", 0)
        docperm.email = p.get("email", 0)
        docperm.share = p.get("share", 0)
        docperm.save(ignore_permissions=True) if existing else docperm.insert(ignore_permissions=True)

    for p in perms:
        frappe.clear_cache(doctype=p["parent"])
