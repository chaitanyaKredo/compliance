import frappe
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("api", allow_site=True, file_count=50)

def calculate_next_dates(due_date, start_date, end_date, frequency):
    next_dates = []
    while due_date <= end_date:
        next_due_date = None
        next_start_date = None
        if frequency == "Daily":
            next_due_date = due_date + timedelta(days=1)
            next_start_date = start_date + timedelta(days=1)
        elif frequency == "Annual":
            next_due_date = due_date + relativedelta(years=1)
            next_start_date = start_date + relativedelta(years=1)
            if due_date.day != next_due_date.day:
                next_due_date = next_due_date.replace(day=28)
                next_start_date = start_date.replace(day=28)
        elif frequency == "Event based":
            next_due_date = due_date
            next_start_date = start_date
        elif frequency == "Half-yearly":
            next_due_date = due_date + relativedelta(months=6)
            next_start_date = start_date + relativedelta(months=6)
            if due_date.day != next_due_date.day:
                next_due_date = next_due_date.replace(day=28)
                next_start_date = start_date.replace(day=28)
        elif frequency == "One time":
            next_due_date = due_date
            next_start_date = start_date
        elif frequency == "Quarterly":
            next_due_date = due_date + relativedelta(months=3)
            next_start_date = start_date + relativedelta(months=3)
            if due_date.day != next_due_date.day:
                next_due_date = next_due_date.replace(day=28)
                next_start_date = start_date.replace(day=28)
        elif frequency == "Renewal":
            next_due_date = due_date + relativedelta(years=1)
            next_start_date = start_date + relativedelta(years=1)
            if due_date.day != next_due_date.day:
                next_due_date = next_due_date.replace(day=28)
                next_start_date = start_date.replace(day=28)
        elif frequency == "Monthly":
            next_due_date = due_date + relativedelta(months=1)
            next_start_date = start_date + relativedelta(months=1)
            if due_date.day != next_due_date.day:
                next_due_date = next_due_date.replace(day=28)
                next_start_date = start_date.replace(day=28)
        else:
            raise ValueError("Invalid frequency option")
        next_dates.append(
            {
                "next_start_date": next_start_date.strftime("%Y-%m-%d"),
                "next_due_date": next_due_date.strftime("%Y-%m-%d"),
            }
        )
        start_date = next_start_date
        due_date = next_due_date
    return next_dates


def is_in_list(a, list):
    found = False
    for item in list:
        if all(a[key] == item[key] for key in a):
            found = True
            break


def make_repeated_entries_for_tasks():
    compliance_assignments = frappe.db.get_all("Complianceassignment", fields=["*"])
    for assignment in compliance_assignments:
        compliancetracker = frappe.db.get_value(
            "Compliancetracker", assignment.compliance, ["*"], as_dict=1
        )
        frequency = compliancetracker.get("frquency")
        due_date = compliancetracker.duedate
        end_date = compliancetracker.enddate
        start_date = compliancetracker.startdate
        next_dates = calculate_next_dates(due_date, start_date, end_date,frequency)
        for next_date_obj in next_dates:
            next_start_date = next_date_obj.get("next_start_date")
            next_due_date = next_date_obj.get("next_due_date")
            if not {"route":assignment.route,"duedate":next_due_date,"startdate":next_start_date} in compliance_assignments:
                new_assignment = frappe.new_doc("Complianceassignment")
                new_assignment.compliance = compliancetracker.name
                new_assignment.route = assignment.route
                new_assignment.start_date = next_start_date
                new_assignment.due_date = next_due_date
                new_assignment.insert()
