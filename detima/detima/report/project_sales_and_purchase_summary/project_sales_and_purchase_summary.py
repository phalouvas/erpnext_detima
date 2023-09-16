# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

from frappe import _
import frappe

def execute(filters=None):
    columns = [
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": 150,
        },
        {
            "fieldname": "total_sales",
            "label": _("Total Sales Invoice Amount"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "total_purchase",
            "label": _("Total Purchase Invoice Amount"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "tax_purchase",
            "label": _("Total Purchase Tax Amount"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "grand_purchase",
            "label": _("Grand Total Purchase Tax Amount"),
            "fieldtype": "Currency",
            "width": 150,
        },
    ]

    data = []

    # Query to calculate the total sales and purchase amounts for each project
    query = """
        SELECT
            p.name AS project,
            SUM(si.total) AS total_sales,
            SUM(si.total_taxes_and_charges) AS tax_sales,
            SUM(si.grand_total) AS grand_sales,
            SUM(pi.total) AS total_purchase,
            SUM(pi.total_taxes_and_charges) AS tax_purchase,
            SUM(pi.grand_total) AS grand_purchase
        FROM
            `tabProject` p
        LEFT JOIN
            `tabSales Invoice` si ON p.name = si.project
        LEFT JOIN
            `tabPurchase Invoice` pi ON p.name = pi.project
        WHERE
            p.status = 'Open'
            AND pi.docstatus = 1
            AND si.docstatus = 1
    """

    status = filters.get("status")
    if filters:
        if status:
            query += f" AND p.status = '{status}'"

    query += "GROUP BY p.name"
    data = frappe.db.sql(query, as_dict=True)

    return columns, data
