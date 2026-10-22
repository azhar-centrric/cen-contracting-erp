import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_purchase_invoice_properties():
    # Hide Series for consistency with Quotation/Sales Invoice (no naming rule here yet, but kept uniform)
    make_property_setter("Purchase Invoice", "naming_series", "hidden", "1", "Check")
