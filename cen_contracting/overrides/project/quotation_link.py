def add_quotation_connection(data):
    # Quotation has no standard "project" field (only Sales Order/Sales Invoice do), so the
    # Project Connections tab never picks it up through the default fieldname - it links a
    # Project through cen_choose_project instead (see overrides/quotation/project_creation.py).
    data.setdefault("non_standard_fieldnames", {})["Quotation"] = "cen_choose_project"

    for group in data.get("transactions", []):
        if group.get("label") == "Sales":
            if "Quotation" not in group["items"]:
                group["items"].insert(0, "Quotation")
            break
    else:
        data["transactions"].append({"label": "Sales", "items": ["Quotation"]})

    return data
