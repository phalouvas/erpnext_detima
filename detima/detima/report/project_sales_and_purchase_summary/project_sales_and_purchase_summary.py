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
            "label": _("Sales Amount"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "total_purchase",
            "label": _("Purchase Amount"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "total_difference",
            "label": _("Difference Amount"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "tax_sales",
            "label": _("Sales Tax"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "tax_purchase",
            "label": _("Purchase Tax"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "tax_difference",
            "label": _("Difference Tax"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "grand_sales",
            "label": _("Sales Total"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "grand_purchase",
            "label": _("Purchase Total"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "grand_difference",
            "label": _("Difference Total"),
            "fieldtype": "Currency",
            "width": 150,
        }
    ]

    result = []

    # Query to calculate the total sales and purchase amounts for each project
    query = """
        SELECT
            p.name AS project,
            COALESCE(si.total_sales, 0) AS total_sales,
            COALESCE(pi.total_purchase, 0) AS total_purchase,
            COALESCE(si.total_sales, 0) - COALESCE(pi.total_purchase, 0) AS total_difference,
            COALESCE(si.tax_sales, 0) AS tax_sales,
            COALESCE(pi.tax_purchase, 0) AS tax_purchase,
            COALESCE(si.tax_sales, 0) - COALESCE(pi.tax_purchase, 0) AS tax_difference,
            COALESCE(si.grand_sales, 0) AS grand_sales,
            COALESCE(pi.grand_purchase, 0) AS grand_purchase,
            COALESCE(si.grand_sales, 0) - COALESCE(pi.grand_purchase, 0) AS grand_difference
        FROM
            `tabProject` p
        LEFT JOIN (
            SELECT
                project,
                SUM(total) AS total_sales,
                SUM(total_taxes_and_charges) AS tax_sales,
                SUM(grand_total) AS grand_sales
            FROM
                `tabSales Invoice`
            WHERE
                docstatus = 1
            GROUP BY
                project
        ) si ON p.name = si.project
        LEFT JOIN (
            SELECT
                project,
                SUM(total) AS total_purchase,
                SUM(total_taxes_and_charges) AS tax_purchase,
                SUM(grand_total) AS grand_purchase
            FROM
                `tabPurchase Invoice`
            WHERE
                docstatus = 1
            GROUP BY
                project
        ) pi ON p.name = pi.project
    """

    status = filters.get("status")
    if filters:
        if status:
            query = query + f" WHERE p.status = '{status}'"

    query = query + f" GROUP BY p.name"
    result = frappe.db.sql(query, as_dict=True)

    return columns, result
