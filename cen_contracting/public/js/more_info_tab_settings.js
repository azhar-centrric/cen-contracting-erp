// Users already in the list shouldn't show up again when picking a new row's User, so duplicates
// can't even be selected (the server-side check in more_info_tab_settings.py still blocks them on
// Save too, in case a row is added some other way).
frappe.ui.form.on("More Info Tab Settings", {
	refresh(frm) {
		frm.set_query("user", "hidden_for_users", function (doc, cdt, cdn) {
			const other_users = (doc.hidden_for_users || [])
				.filter((row) => row.name !== cdn)
				.map((row) => row.user)
				.filter(Boolean);

			return {
				filters: [["User", "name", "not in", other_users]],
			};
		});
	},
});
