// cen_payment_terms is an Autocomplete listing the enabled Payment Term Options, while still
// accepting a typed term for the cases where a customer's terms differ from the standard ones
const PAYMENT_TERM_OPTION = 'cen_contracting.cen_contracting.doctype.payment_term_option.payment_term_option';

["Quotation", "Sales Order", "Sales Invoice"].forEach((doctype) => {
    frappe.ui.form.on(doctype, {
        setup: function(frm) {
            frm.set_df_property('cen_payment_terms', 'ignore_validation', 1);
            frm.set_query('cen_payment_terms', () => ({
                query: `${PAYMENT_TERM_OPTION}.get_payment_term_options`
            }));
        },
        onload: function(frm) {
            // New documents start with the default term; ones created from another document keep the copied term
            if (frm.is_new() && !frm.doc.cen_payment_terms) {
                frappe.call(`${PAYMENT_TERM_OPTION}.get_default_payment_term`).then(({ message }) => {
                    if (message && !frm.doc.cen_payment_terms) {
                        frm.set_value('cen_payment_terms', message);
                    }
                });
            }
        }
    });
});
