# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = []
    columns.append(
			dict(
				label=_("Invoice"),
				fieldname="Invoice",
				fieldtype="data",
				options=None,
				width="100",
			)
		)
    columns.append(
			dict(
				label=_("Name"),
				fieldname="Name",
				fieldtype="data",
				options=None,
				width="100",
			)
		)
    columns.append(
		dict(
			label=_("Posting Date"),
			fieldname="Posting Date",
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
				label=_("Amount Running Balance"),
				fieldname="Amount Running Balance",
				fieldtype="Currency",
				options="Company:company:default_currency",
				width="100",
			)
		)
    columns.append(
			dict(
				label=_("Tax"),
				fieldname="Tax",
				fieldtype="Currency",
				options="Company:company:default_currency",
				width="100",
			)
		)
    columns.append(
			dict(
				label=_("Tax Running Balance"),
				fieldname="Tax Running Balance",
				fieldtype="Currency",
				options="Company:company:default_currency",
				width="100",
			)
		)
    columns.append(
			dict(
				label=_("Total"),
				fieldname="Total",
				fieldtype="Currency",
				options="Company:company:default_currency",
				width="100",
			)
		)
    columns.append(
			dict(
				label=_("Total Running Balance"),
				fieldname="Total Running Balance",
				fieldtype="Currency",
				options="Company:company:default_currency",
				width="100",
			)
		)

    result = []

    project_name = filters.get("project")
    date_from = filters.get("period_start_date")
    date_to = filters.get("period_end_date")

    # Query for sales invoices sorted by posting date
    query_sales = """
    SELECT
        si.name AS 'Invoice',
        si.customer AS 'Name',
        si.posting_date AS 'Posting Date',
        'Sales' AS 'Invoice Type',
        si.total AS 'Amount',
        si.total_taxes_and_charges AS 'Tax',
        si.grand_total AS 'Total'
    FROM
        `tabSales Invoice` si
    WHERE
        si.project = %(project_name)s
        AND si.posting_date BETWEEN %(date_from)s AND %(date_to)s
        AND si.docstatus = 1
    ORDER BY 
        'Posting Date'
    """

    # Query for purchase invoices sorted by posting date
    query_purchase = """
    SELECT
        pi.name AS 'Invoice',
        pi.supplier AS 'Name',
        pi.posting_date AS 'Posting Date',
        'Purchase' AS 'Invoice Type',
        (-1 * pi.total) AS 'Amount',
        (-1 * pi.total_taxes_and_charges) AS 'Tax',
        (-1 * pi.grand_total) AS 'Total'
    FROM
        `tabPurchase Invoice` pi
    WHERE
        pi.project = %(project_name)s
        AND pi.posting_date BETWEEN %(date_from)s AND %(date_to)s
        AND pi.docstatus = 1
    ORDER BY 
        'Posting Date'
    """

    # Execute both SQL queries
    query_sales_result = frappe.db.sql(query_sales, {"project_name": project_name, "date_from": date_from, "date_to": date_to}, as_dict=True)
    query_purchase_result = frappe.db.sql(query_purchase, {"project_name": project_name, "date_from": date_from, "date_to": date_to}, as_dict=True)

    # Merge the results and sort them by date
    merged_result = sorted(query_sales_result + query_purchase_result, key=lambda x: x.get('Posting Date'))

    amount_running_balance = 0
    tax_running_balance = 0
    total_running_balance = 0

    for row in merged_result:
        amount_running_balance = amount_running_balance + row.get('Amount')
        tax_running_balance = tax_running_balance + row.get('Tax')
        total_running_balance = total_running_balance + row.get('Total')

        row['Amount Running Balance'] = amount_running_balance
        row['Tax Running Balance'] = tax_running_balance
        row['Total Running Balance'] = total_running_balance
        result.append(row)

    return columns, result