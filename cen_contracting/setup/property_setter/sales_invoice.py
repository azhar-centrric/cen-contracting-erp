import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_sales_invoice_properties():
    # Hide Series: a Document Naming Rule (prefix CC/26/) overrides whatever this field
    # shows, so leaving it visible confuses users into thinking it reflects the real name.
    make_property_setter("Sales Invoice", "naming_series", "hidden", "1", "Check")

    make_property_setter("Sales Invoice", "payment_schedule_section", "hidden", "1", "Check")

    # Always show Description and UOM in the items table; shrink other columns so all fit in the grid's 10 units
    # (Warehouse keeps its default 2 units and only shows when Update Stock is ticked)
    make_property_setter("Sales Invoice Item", "description", "in_list_view", 1, "Check")
    make_property_setter("Sales Invoice Item", "uom", "in_list_view", 1, "Check")
    for fieldname, columns in {"item_code": 2, "description": 2, "qty": 1, "uom": 1, "rate": 1, "amount": 1}.items():
        make_property_setter("Sales Invoice Item", fieldname, "columns", columns, "Int")
