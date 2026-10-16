# Quotation - Customizations & Logic

## 1. Custom Fields & Data Mapping
* **Company & Customer Details:** Handled via standard ERPNext fields (`company`, `party_name`, `customer_address`).
* **Attention To:** Handled via standard `contact_person` field. Will be formatted as "Attention To: [Name]" on the print format.
* **Customer Reference / LPO:** Custom field `cen_lpo_number` created (Data field).
* **Payment Terms:** Standard `payment_terms_template` is used for tabular schedules. Custom field `cen_payment_terms` holds the payment term as a dropdown with manual entry allowed (see section 5).
* **Project Syncing:** Custom fields (`cen_project_name`, `cen_choose_project`, `cen_project_type`) migrated and active. UI filtering managed by `project_filters.js`.


## 2. Validation & Pricing Logic
* **Validity Date Bypass:** The standard mandatory requirement for `valid_till` (Quotation Expiry) has been disabled via a backend Property Setter (`setup/property_setter/quotation.py`) to allow open-ended quotations.
* **SQM Pricing Strategy:** No custom code is required for SQM pricing. The requirement for quotations to be primarily entered on a per SQM basis will be handled natively by configuring the Default Sales UOM to "Sqm" on the respective Item Masters.

## 3. Revision History & Version Control
* **Auto-Incrementing Versions:** A Python hook (`before_insert` in `overrides/quotation/version_control.py`) checks if a quotation is being amended. If true, it automatically fetches the `cen_version_number` of the cancelled quote and increments it by 1 on the new draft.
* **Custom UI Revision Flow:** A client script (`public/js/quotation.js`) intercepts the standard amendment flow on cancelled quotations. It replaces the native "Amend" button with a "Revise Quotation" dialog, requiring the user to log a reason before automatically passing it to the new draft.

## 4. Items Table Layout
* **Description & UOM Always Visible:** `description` and `uom` are shown as columns in the items table (`in_list_view`) via Property Setters in `setup/property_setter/quotation.py`.
* **Column Widths:** Item Code 2, Description 3, Qty 1, UOM 1, Rate 1, Amount 2 (the grid holds 10 units; Frappe widens columns automatically when space is free).

## 5. Payment Term Dropdown
* **Field:** Custom field `cen_payment_terms` (Payment Term) is an `Autocomplete` field. It lists the enabled records of the **Payment Term Option** master (`cen_contracting/doctype/payment_term_option/`), so users pick a standard term instead of typing it every time.
* **Manual Entry:** When a customer's terms differ, users can still type any text. `public/js/payment_terms.js` sets `ignore_validation` on the field so typed values are kept, and loads the list through `get_payment_term_options` (whitelisted in `payment_term_option.py`, disabled options hidden).
* **Default Term:** Ticking **Default** on a Payment Term Option fills it in automatically on new documents whose Payment Term is empty (`get_default_payment_term`, called from `payment_terms.js` on load) and lists it first in the dropdown. Documents created from another document keep the copied term. Only one option can be default (ticking it clears the others), and the default can't be disabled.
* **Managing Options:** Add, edit or disable terms in the Payment Term Option list (System Manager and Sales Manager can edit; Sales User and Accounts User can read).
* **Conversion Patch:** The field was originally `Data`. Frappe doesn't allow Data -> Autocomplete on a Custom Field, so `patches/payment_terms_to_autocomplete.py` switches it in place during `bench migrate` (both are varchar(140), existing values are kept).
