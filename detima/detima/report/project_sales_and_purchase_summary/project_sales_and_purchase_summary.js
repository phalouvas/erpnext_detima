// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Sales and Purchase Summary"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ["Open", "Completed", "Cancelled"],
			"default": "Open",
			"reqd": 1
		}
	]
};
