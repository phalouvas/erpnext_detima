# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = []
    columns.append(
			dict(
				label=_("Sales Invoice"),
				fieldname="Sales Invoice",
				fieldtype="Dynamic Link",
				options=None,
				width="100",
			)
		)
    columns.append(
		dict(
			label=_("Sales Invoice Date"),
			fieldname="Sales Invoice Date",
			fieldtype="Date",
			options=None,
			width="100",
		)
	)
    columns.append(
			dict(
				label=_("Purchase Invoice"),
				fieldname="Purchase Invoice",
				fieldtype="Dynamic Link",
				options=None,
				width="100",
			)
		)
    columns.append(
		dict(
			label=_("Purchase Invoice Date"),
			fieldname="Purchase Invoice Date",
			fieldtype="Date",
			options=None,
			width="100",
		)
	)
    columns.append(
			dict(
				label=_("Invoice Type"),
				fieldname="Invoice Type",
				fieldtype="data",
				options=None,
				width="100",
			)
		)
    columns.append(
			dict(
				label=_("Amount"),
				fieldname="Amount",
				fieldtype="Currency",
				options="Company:company:default_currency",
				width="100",
			)
		)
    columns.append(
			dict(
				label=_("Running Balance"),
				fieldname="Running Balance",
				fieldtype="Currency",
				options="Company:company:default_currency",
				width="100",
			)
		)

    data = []

    project_name = filters.get("project")
    date_from = filters.get("period_start_date")
    date_to = filters.get("period_end_date")

    # Query for sales invoices sorted by posting date
    query_sales = """
    SELECT
        si.name AS 'Sales Invoice',
        si.posting_date AS 'Sales Invoice Date',
        NULL AS 'Purchase Invoice',
        NULL AS 'Purchase Invoice Date',
        'Sales' AS 'Invoice Type',
        si.total AS 'Amount'
    FROM
        `tabSales Invoice` si
    WHERE
        si.project = %(project_name)s
        AND si.posting_date BETWEEN %(date_from)s AND %(date_to)s
    ORDER BY 
        'Sales Invoice Date'
    """

    # Query for purchase invoices sorted by posting date
    query_purchase = """
    SELECT
        NULL AS 'Sales Invoice',
        NULL AS 'Sales Invoice Date',
        pi.name AS 'Purchase Invoice',
        pi.posting_date AS 'Purchase Invoice Date',
        'Purchase' AS 'Invoice Type',
        pi.total AS 'Amount'
    FROM
        `tabPurchase Invoice` pi
    WHERE
        pi.project = %(project_name)s
        AND pi.posting_date BETWEEN %(date_from)s AND %(date_to)s
    ORDER BY 
        'Purchase Invoice Date'
    """

    # Execute both SQL queries
    query_sales_result = frappe.db.sql(query_sales, {"project_name": project_name, "date_from": date_from, "date_to": date_to}, as_dict=True)
    query_purchase_result = frappe.db.sql(query_purchase, {"project_name": project_name, "date_from": date_from, "date_to": date_to}, as_dict=True)

    # Merge the results and sort them by date
    merged_result = sorted(query_sales_result + query_purchase_result, key=lambda x: x.get('Sales Invoice Date') or x.get('Purchase Invoice Date'))

    running_balance = 0
    total = 0  # Initialize the total

    for row in merged_result:
        if row.get('Invoice Type') == 'Sales':
            running_balance += row.get('Amount')
            total += row.get('Amount')  # Add the amount to the total for sales invoices
        elif row.get('Invoice Type') == 'Purchase':
            running_balance -= row.get('Amount')
            total -= row.get('Amount')  # Subtract the amount from the total for purchase invoices

        # Add the 'Total' column to the row
        row['Total'] = total

        row['Running Balance'] = running_balance
        data.append(row)

    return columns, data