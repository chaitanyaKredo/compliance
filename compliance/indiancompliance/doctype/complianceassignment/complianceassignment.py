# Copyright (c) 2023, chaitanya and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.data import getdate, add_days, today, add_months
from frappe.model.document import Document


def notification_required(frequency):
    eligible_frequencies = ["Daily", "Monthly", "Quarterly","Half-yearly","Annual"]
    return  frequency in eligible_frequencies

def has_auto_repeat(doc_type, doc_name):
    auto_repeat_count = frappe.db.count("Auto Repeat",
                                        filters={"reference_doctype": doc_type, "reference_document": doc_name})
    print(doc_type)
    return auto_repeat_count > 0

def create_notification(source_doc, compliance,custom_values):
    notification = frappe.new_doc("Notification")
    notification.name = source_doc.name + custom_values.get("name")
    notification.subject = compliance.title
    notification.document_type = "Complianceassignment"
    notification.event = "Days Before"
    notification.date_changed = "duedate"
    notification.days_in_advance = custom_values.get("before")
    notification.append(
        "recipients", {"receiver_by_document_field": custom_values.get("receiver")})
    notification.send_to_all_assignees = 1
    notification.send_system_notification = 1
    notification.send_to_all_assignees = 1
    notification.message = custom_values.get("message")
    notification.save()

def make_auto_repeat(**args):
    args = frappe._dict(args)
    doc = frappe.get_doc(
        {
            "doctype": "Auto Repeat",
            "reference_doctype": args.reference_doctype or "ToDo",
            "reference_document": args.reference_document or frappe.db.get_value("ToDo", "name"),
            "submit_on_creation": args.submit_on_creation or 0,
            "frequency": args.frequency or "Daily",
            "start_date": args.start_date or add_days(today(), -1),
            "end_date": args.end_date or "",
            "notify_by_email": args.notify or 0,
            "recipients": args.recipients or "",
            "subject": args.subject or "",
            "message": args.message or "",
            "repeat_on_days": args.days or [],
        }
    ).insert(ignore_permissions=True)

class Complianceassignment(Document):
	def after_insert(self):
		compliance = frappe.get_doc("Compliancetracker", self.compliance)
		reminder = {
            		"name": "_reminder",
            		"before": compliance.get("reminderbefore"),
            		"email": self.assignedto,
            		"message": "This is the reminder on task",
            		"receiver": "assignedto"
        		}
		escalation = {
			"name": "_escalate",
            		"before": compliance.get("escalate"),
            		"email": self.supervisor,
            		"message": f'This is the reminder that , a task is due in {compliance.get("escalate")} days',
            		"receiver": "supervisor"
        		}
		create_notification(self, compliance, escalation)
		create_notification(self, compliance, reminder)
		if not has_auto_repeat("Complianceassignment", self.name):
            			make_auto_repeat(frequency=compliance.get("frequency"),
                             	reference_doctype="Complianceassignment",
                             	reference_document=self.name,
                             	start_date=compliance.get("startdate"),
                             	end_date=compliance.get("enddate"),
                             	submit_on_creation=1,
                             	recepients=self.assignedto
                             )

