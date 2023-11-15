import frappe
from event_streaming.event_streaming.doctype.event_update_log.event_update_log import (
    make_event_update_log,
)


def create_logs():
    docs = frappe.get_list("Compliancetracker", fields=["*"])
    for doc in docs:
        if not doc.flags.event_update_log:
            make_event_update_log(doc, update_type="Create")

