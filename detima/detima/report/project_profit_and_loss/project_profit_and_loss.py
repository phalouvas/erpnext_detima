# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = [
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
        },
		{
            "fieldname": "account",
            "label": _("Account"),
            "fieldtype": "Link",
            "options": "Account",
        },
		{
            "fieldname": "total_difference",
            "label": _("Amount"),
            "fieldtype": "Currency",
        },
	]

	period_start_date = filters.get("period_start_date")
	period_end_date = filters.get("period_end_date")
	
	# Query to calculate the total sales and purchase amounts for each project
	query = """
        SELECT
            p.name AS project,
            COALESCE(si.total_sales, 0) AS total_sales,
            COALESCE(pi.total_purchase, 0) AS total_purchase,
            COALESCE(si.total_sales, 0) - COALESCE(pi.total_purchase, 0) AS total_difference
        FROM
            `tabProject` p
        LEFT JOIN (
            SELECT
                project,
                SUM(total) AS total_sales
            FROM
                `tabSales Invoice`
            WHERE
                docstatus = 1
			AND
				posting_date BETWEEN %(period_start_date)s AND %(period_end_date)s
            GROUP BY
                project
        ) si ON p.name = si.project
        LEFT JOIN (
            SELECT
                project,
                SUM(total) AS total_purchase
            FROM
                `tabPurchase Invoice`
            WHERE
                docstatus = 1
			AND
				posting_date BETWEEN %(period_start_date)s AND %(period_end_date)s
            GROUP BY
                project
        ) pi ON p.name = pi.project
    """
	status = filters.get("status")
	if filters:
		if status:
			query = query + f" WHERE p.status = '{status}'"

	query = query + f" GROUP BY p.name"
	project_result = frappe.db.sql(query, {"period_start_date": period_start_date, "period_end_date": period_end_date} , as_dict=True)
	
    # Query to calculate total expenses grouped by account
	expenses_query = """
        SELECT
            ai.account AS account,
            SUM(ai.credit - ai.debit) AS total_difference
        FROM
            `tabGL Entry` ai
        LEFT JOIN
            `tabAccount` a ON ai.account = a.name
        WHERE
            ai.docstatus = 1
        AND
            ai.posting_date BETWEEN %(period_start_date)s AND %(period_end_date)s
        AND
            a.root_type = 'Expense'
		AND
            a.report_type = 'Profit and Loss'
        GROUP BY
            ai.account
    """
	
	expenses_result = frappe.db.sql(expenses_query, {"period_start_date": period_start_date, "period_end_date": period_end_date}, as_dict=True)
	
	result = project_result + expenses_result

	return columns, result
