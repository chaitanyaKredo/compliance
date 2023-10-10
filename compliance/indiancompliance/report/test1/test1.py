import frappe

def execute(filters=None):

        columns, data = [], []
        columns = get_columns()
        user = frappe.session.user
        data = frappe.db.get_all("Complianceassignment", filters={"assignedto":user},fields=["compliance","startdate","duedate"])
        return columns, data

def get_columns():
        columns = [
                {"fieldname": "compliance", "fieldtype": "Link", "label": ("Compliance Name"), "options": "compliancetracker", "width": 'auto'},
                {"fieldname": "startdate", "fieldtype": "date", "label": ("Start Date"), "width": 'auto'},
                {"fieldname":"duedate","fieldtype":"date","label":("Due Date"),"width":'auto'}
        ]
        return columns
