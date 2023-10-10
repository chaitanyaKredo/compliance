import frappe

def execute(filters=None):

	columns, data = [], []
	columns = get_columns()
	user = frappe.session.user
	data = frappe.db.get_all("Complianceassignment", filters={"assignedto":user}, fields=["*"])
	return columns, data

def get_columns():
	columns = [
		{"fieldname": "compliance", "fieldtype": "Link", "label": ("Compliance Name"), "options": "compliancetracker", "width": 200},
		{"fieldname": "startdate", "fieldtype": "date", "label": ("Start Date"), "width": 200},
		{"fieldname":"duedate","fieldtype":"date"."label":("Due Date"),"width":200}
	]
	return columns
