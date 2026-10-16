# Sales Invoice - Customizations & Logic

## 1. Custom Fields & Data Mapping
* **Project Details:** Custom fields (`cen_project_name`, `cen_choose_project`, `cen_project_type`) mapped to ensure project continuity from the Sales Order.


## 2. Items Table Layout
* **Description & UOM Always Visible:** `description` and `uom` are shown as columns in the items table (`in_list_view`) via Property Setters in `setup/property_setter/sales_invoice.py`.
* **Column Widths:** Item Code 2, Description 2, Qty 1, UOM 1, Rate 1, Amount 1. The standard Warehouse column (2 units) still appears only when Update Stock is ticked.

## 3. Payment Term Dropdown
* **Field:** Custom field `cen_payment_terms` (Payment Term) is an `Autocomplete` field, copied from the Sales Order (same fieldname). It lists the enabled records of the **Payment Term Option** master (`cen_contracting/doctype/payment_term_option/`), so users pick a standard term instead of typing it every time.
* **Manual Entry:** When a customer's terms differ, users can still type any text. `public/js/payment_terms.js` sets `ignore_validation` on the field so typed values are kept, and loads the list through `get_payment_term_options` (whitelisted in `payment_term_option.py`, disabled options hidden).
* **Default Term:** Ticking **Default** on a Payment Term Option fills it in automatically on new documents whose Payment Term is empty (`get_default_payment_term`, called from `payment_terms.js` on load) and lists it first in the dropdown. Documents created from another document keep the copied term. Only one option can be default (ticking it clears the others), and the default can't be disabled.
* **Managing Options:** Add, edit or disable terms in the Payment Term Option list (System Manager and Sales Manager can edit; Sales User and Accounts User can read).
* **Conversion Patch:** The field was originally `Data`. Frappe doesn't allow Data -> Autocomplete on a Custom Field, so `patches/payment_terms_to_autocomplete.py` switches it in place during `bench migrate` (both are varchar(140), existing values are kept).
