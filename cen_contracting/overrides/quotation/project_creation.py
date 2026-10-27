import frappe


def create_project_for_new_type(doc, method=None):
    # Project Type "New" + a typed Project Name means this quotation wants a brand-new Project
    # instead of linking an existing one via cen_choose_project. Previously nothing acted on
    # that until someone manually created a Project later (typically from the Sales Order) and
    # typed the same name in themselves. This creates it as soon as the Quotation is saved.
    if doc.get("cen_project_type") != "New":
        return

    project_name = doc.get("cen_project_name")
    if not project_name:
        return

    # Already linked (by a previous save of this same quotation) - never create a second
    # Project for it. Quotation has no standard "project" field of its own (only Sales Order and
    # Sales Invoice do), so cen_choose_project is the only thing to check here.
    if doc.get("cen_choose_project"):
        return

    # No customer set here, deliberately: ERPNext's own validate_proj_cust (Sales Order and
    # Sales Invoice) blocks saving a document whose customer differs from its Project's customer,
    # unless the Project's customer is blank. The client wants to freely rebill a Quotation's
    # project to a different customer at Sales Order/Invoice stage, so the Project is left
    # customer-agnostic rather than locked to whoever the originating Quotation was for.
    project = frappe.get_doc(
        {
            "doctype": "Project",
            "project_name": project_name,
            "company": doc.company,
            "expected_start_date": doc.transaction_date,
        }
    )
    # cen_project_supervisor is mandatory on Project, but nothing on the Quotation says who that
    # should be - leave it blank for whoever picks up the project to fill in, rather than guess.
    project.insert(ignore_permissions=True, ignore_mandatory=True)

    # cen_contracting's sync_projects_on_validate (also on Quotation's validate) carries this
    # into the standard "project" field on whatever gets made from this quotation (e.g. a mapped
    # Sales Order), the same way it already does for an existing project chosen via
    # cen_choose_project.
    doc.cen_choose_project = project.name
