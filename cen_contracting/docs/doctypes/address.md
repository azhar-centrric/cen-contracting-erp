# Address - Customizations & Logic

## 1. City Not Mandatory
* Frappe's standard Address doctype makes `city` mandatory. The client doesn't always have a city for a new Customer's address, so it was blocking Customer creation.
* `setup/property_setter/address.py` (`set_address_properties`) sets `reqd=0` on `city` via a Property Setter.
