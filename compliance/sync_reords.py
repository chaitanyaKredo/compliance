import frappe

frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("api", allow_site=True, file_count=50)

def sync_logs(consumer, doc, update_log):
    result = frappe.db.sql("select * from tabComplianceassignment LIMIT 2")
    logger.info(f"{result},{consumer}")
    return True
