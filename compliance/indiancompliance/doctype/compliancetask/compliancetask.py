# Copyright (c) 2023, chaitanya and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.data import getdate, add_days, today, add_months


def has_auto_repeat(doc_type, doc_name):
    auto_repeat_count = frappe.db.count("Auto Repeat",
                                        filters={"reference_doctype": doc_type, "reference_document": doc_name})

    return auto_repeat_count > 0


class Compliancetask(WebsiteGenerator):
    def before_insert(self):
        self.escalate = 2

    def after_insert(self):
        reminder = {
            "name": "_reminder",
            "before": self.reminderbefore,
            "email": self.assignedto,
            "message": "This is the reminder on task",
            "receiver": "assignedto"
        }
        escalation = {
            "name": "_escalate",
            "before": self.escalate,
            "email": self.supervisor,
            "message": f'This is the reminder that , a task is due in {self.escalate} days',
            "receiver": "supervisor"
        }
        create_notification(self, escalation)
        create_notification(self, reminder)
        if not has_auto_repeat("Compliancetask", self.name):
            make_auto_repeat(frequency=self.frequency,
                             reference_doctype="Compliancetask",
                             reference_document=self.name,
                             start_date=self.startdate,
                             submit_on_creation=1,
                             recepients=self.assignedto
                             )


def create_notification(source_doc, custom_values):
    notification = frappe.new_doc("Notification")
    notification.name = source_doc.name + custom_values.get("name")
    notification.subject = source_doc.section
    notification.document_type = "Compliancetask"
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

    return doc


def generate_compliance_tasks():
    compliance_tasks = frappe.get_all(
        "Compliancetask", filters={}, fields=["*"])
    for task in compliance_tasks:
        next_due_date = calculate_next_due_date(task)
        create_new_task(task, next_due_date)


def calculate_next_due_date(task):
    if task.frequency == "Daily":
        return add_days(task.duedate, 1)
    elif task.frequency == "Annual":
        return add_months(task.duedate, 12)
    elif task.frequency == "Half-yearly":
        return add_months(task.duedate, 6)
    elif task.frequency == "Quarterly":
        return add_months(task.duedate, 3)
    elif task.frequency == "Event-based":
        return task.duedate
    else:
        return task.duedate


def create_new_task(task, next_due_date):
    new_task = frappe.new_doc("Compliancetask")
    new_task.function = task.function
    new_task.section = task.section
    new_task.applicability = task.applicability
    new_task.location = task.location
    new_task.frequency = task.frequency
    new_task.risk = task.risk
    new_task.assignedto = task.assignedto
    new_task.supervisor = task.supervisor
    new_task.type = task.type
    new_task.status = task.status
    new_task.escalate = task.escalate
    new_task.reminderbefore = task.reminderbefore
    new_task.startdate = next_due_date
    new_task.duedate = calculate_next_due_date(new_task)
    new_task.enddate = task.enddate
    print(new_task)
    new_task.save()
