# Copyright (c) 2023, chaitanya and contributors
# For license information, please see license.txt

import frappe
import datetime

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	current_date = datetime.date.today()
	data = frappe.db.get_all("Complianceassignment", filters={"duedate": ("<", current_date)}, fields=["*"])
	return columns, data

def get_columns():
	columns = [
		{"fieldname": "name", "fieldtype": "Link", "label": ("Access Link"), "options": "Complianceassignment", "width": 150},
		{"fieldname": "route", "fieldtype": "data", "label": ("Task Name"), "width": 400},
                {"fieldname": "assignedto", "fieldtype": "data", "label": ("User"), "width": 200},
                {"fieldname":"duedate","fieldtype":"date","label":("Due Date"),"width":200},
		{"fieldname": "compliance", "fieldtype": "Link", "label": ("Compliance"), "options": "Compliancetracker", "width": 400}
        ]
	return columns
