import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_address_properties():
    # City is mandatory on Frappe's standard Address doctype - the client doesn't always have it
    # (e.g. when creating a Customer with only a partial address), so it blocked saving.
    make_property_setter("Address", "city", "reqd", "0", "Check")
