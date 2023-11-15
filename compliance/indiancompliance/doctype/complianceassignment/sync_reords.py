import frappe

def sync_table(consumer, doc, update_log):
    return frappe.db.sql("""
        SELECT
            COUNT(*)
        FROM `tabCompliancetracker`
    """
