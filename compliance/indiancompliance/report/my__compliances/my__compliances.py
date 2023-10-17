# Copyright (c) 2023, chaitanya and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import get_link_to_form

def execute(filters=None):
        columns, data = [], []
        columns = get_columns()
        user = frappe.session.user
        response = frappe.db.get_all("Complianceassignment", filters={"assignedto":user},fields=["*"])
        for record in response:
                record['form_link'] = get_link_to_form("Complianceassignment",record["name"])
                record['function']  = frappe.db.get_value("Compliancetracker",record["compliance"],"function")
                data.append(record)
        return columns, data

def get_columns():
        columns = [
                {"fieldname": "compliance", "fieldtype": "Link", "label": ("Compliance Name"),"options":"Compliancetracker" ,"width": 400},
                {"fieldname":"supervisor", "fieldtype": "data", "label": ("Supervisor"), "width": 200},
                {"fieldname":"duedate","fieldtype":"date","label":("Due Date"),"width":200},
                {"fieldname":"form_link","fieldtype":"Dynamic_Link","label":("Access Link"),"width":200},
                {"fieldname":"function","fieldtype":"data","label":("Function"),"width":200},
        ]
        return columns
