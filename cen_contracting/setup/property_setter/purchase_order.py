import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_purchase_order_properties():
    # Hide Series for consistency with Quotation/Sales Invoice (no naming rule here yet, but kept uniform)
    make_property_setter("Purchase Order", "naming_series", "hidden", "1", "Check")
