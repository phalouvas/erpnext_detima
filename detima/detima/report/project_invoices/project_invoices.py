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
				fieldtype="Link",
				options="Sales Invoice",
				width="100",
			)
		)
    columns.append(
			dict(
				label=_("Purchase Invoice"),
				fieldname="Purchase Invoice",
				fieldtype="Link",
				options="Purchase Invoice",
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

    # Query for sales invoices sorted by posting date
    query_sales = """
    SELECT
        si.name AS 'Sales Invoice',
        si.customer AS 'Name',
        si.posting_date AS 'Posting Date',
        si.total AS 'Amount',
        si.total_taxes_and_charges AS 'Tax',
        si.grand_total AS 'Total'
    FROM
        `tabSales Invoice` si
    WHERE
        si.project = %(project_name)s
        AND si.docstatus = 1
    ORDER BY 
        'Posting Date'
    """

    # Query for purchase invoices sorted by posting date
    query_purchase = """
    SELECT
        pi.name AS 'Purchase Invoice',
        pi.supplier AS 'Name',
        pi.posting_date AS 'Posting Date',
        (-1 * pi.total) AS 'Amount',
        (-1 * pi.total_taxes_and_charges) AS 'Tax',
        (-1 * pi.grand_total) AS 'Total'
    FROM
        `tabPurchase Invoice` pi
    WHERE
        pi.project = %(project_name)s
        AND pi.docstatus = 1
    ORDER BY 
        'Posting Date'
    """

    # Execute both SQL queries
    query_sales_result = frappe.db.sql(query_sales, {"project_name": project_name}, as_dict=True)
    query_purchase_result = frappe.db.sql(query_purchase, {"project_name": project_name}, as_dict=True)

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