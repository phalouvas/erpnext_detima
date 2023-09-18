// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Invoices"] = {
	"filters": [
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 1
		}
	]
};
