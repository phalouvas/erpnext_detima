// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Profit and Loss"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ["Open", "Completed", "Cancelled"],
			"default": None,
			"reqd": 1
		},
		{
            "fieldname": "period_start_date",
            "label": _("Start Date"),
            "fieldtype": "Date",
            "options": None,
			"reqd": 1
        },
		{
            "fieldname": "period_end_date",
            "label": _("End Date"),
            "fieldtype": "Date",
            "options": None,
			"reqd": 1
        },
	]
};
