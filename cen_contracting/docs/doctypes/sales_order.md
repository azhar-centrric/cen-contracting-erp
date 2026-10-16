# Sales Order - Customizations & Logic

## 1. Custom Fields & Data Mapping
* **Project Details:** Custom fields (`cen_project_name`, `cen_choose_project`, `cen_project_type`) mapped to ensure continuity from Quotation. UI filtering managed by `project_filters.js`.

## 2. Validation Logic
* **Backend Sync:** Standard `project` field automatically synchronized with `cen_choose_project` upon validation via the backend hook (`overrides/opportunity/project_sync.py`).


## 3. Optional Delivery Date
* **Not Mandatory:** `delivery_date` on Sales Order and Sales Order Item is optional, so orders can be saved and submitted without a delivery date.
* **Backend:** ERPNext's `validate_delivery_date` throws "Please enter Delivery Date" on every Sales type order. It is relaxed by the `OptionalDeliveryDateMixin` class (`overrides/sales_order/optional_delivery_date.py`), mapped via `extend_doctype_class` in `hooks.py`. When no date is entered the check is skipped; once a date is entered ERPNext's standard behaviour still applies (dates copied between the order and its items, and a date before the order date is rejected).
* **Frontend:** ERPNext's form script marks the item Delivery Date column mandatory; `public/js/sales_order.js` overrides `toggle_delivery_date` in the `setup` event to keep it optional.
* **Property Setter:** `reqd = 0` on both fields in `setup/property_setter/sales_order.py`, so the fields stay optional even if another app makes them mandatory.

## 4. Items Table Layout
* **Description & UOM Always Visible:** `description` and `uom` are shown as columns in the items table (`in_list_view`) via Property Setters in `setup/property_setter/sales_order.py`.
* **Column Widths:** Item Code 2, Delivery Date 1, Description 2, Qty 1, UOM 1, Rate 1, Amount 2 (the grid holds 10 units; Frappe widens columns automatically when space is free).

## 5. Payment Term Dropdown
* **Field:** Custom field `cen_payment_terms` (Payment Term) is an `Autocomplete` field, copied from the Quotation (same fieldname). It lists the enabled records of the **Payment Term Option** master (`cen_contracting/doctype/payment_term_option/`), so users pick a standard term instead of typing it every time.
* **Manual Entry:** When a customer's terms differ, users can still type any text. `public/js/payment_terms.js` sets `ignore_validation` on the field so typed values are kept, and loads the list through `get_payment_term_options` (whitelisted in `payment_term_option.py`, disabled options hidden).
* **Default Term:** Ticking **Default** on a Payment Term Option fills it in automatically on new documents whose Payment Term is empty (`get_default_payment_term`, called from `payment_terms.js` on load) and lists it first in the dropdown. Documents created from another document keep the copied term. Only one option can be default (ticking it clears the others), and the default can't be disabled.
* **Managing Options:** Add, edit or disable terms in the Payment Term Option list (System Manager and Sales Manager can edit; Sales User and Accounts User can read).
* **Conversion Patch:** The field was originally `Data`. Frappe doesn't allow Data -> Autocomplete on a Custom Field, so `patches/payment_terms_to_autocomplete.py` switches it in place during `bench migrate` (both are varchar(140), existing values are kept).
