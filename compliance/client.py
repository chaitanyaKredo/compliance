import frappe
import json

@frappe.whitelist()
def get_dependent_doctypes(doc1,doc2,filters_doc1,filters_doc2):
	doc1_list = frappe.get_all(doc1,fields=['*'],filters=filters_doc1)
	doc2_list = frappe.get_all(doc2,fields=['*'],filters=filters_doc2)
	return {doc1:doc1_list,doc2:doc2_list}

@frappe.whitelist(methods=["POST", "PUT"])
def update_or_create_records(docname, docdata_list):
    docdata_list = json.loads(docdata_list)
    created_or_updated_records = []
    for docdata in docdata_list:
    	doc = frappe.get_doc(docname, docdata.get('name'))
    	doc.update(docdata)
    	doc.save()
    	created_or_updated_records.append(docdata.get('name'))
    frappe.db.commit()
    return created_or_updated_records

@frappe.whitelist(methods=["POST", "PUT"])
def update_or_create_subscription(docname, payload):
    docdata = json.loads(payload)
    if docdata.get("is_in_list"):
        doc = frappe.get_doc(docname, docdata.get("name"))
        doc.compliance = docdata.get("name")
        doc.issubscribed = docdata.get("is_subscribed")
        doc.save()
    else:
        doc = frappe.new_doc(docname)
        doc.compliance = docdata.get("name")
        doc.issubscribed = docdata.get("is_subscribed")
        doc.save()
    frappe.db.commit()
    return docdata


@frappe.whitelist()
def get_subscribed_doctype_list():
    masters_list = frappe.get_all("Compliancetracker", fields=["*"])
    subscription_list = frappe.get_all("Subscription", fields=["*"])
    subscription_dict = {
        record["name"]: record["issubscribed"] for record in subscription_list
    }
    result_list = []
    for compliance_record in masters_list:
        compliance_name = compliance_record["name"]
        if compliance_name in subscription_dict:
            issubscribed_value = subscription_dict[compliance_name] == 1
            isinsubscription_value = True
        else:
            issubscribed_value = 0
            isinsubscription_value = False
        result_list.append(
            {
                "name": compliance_name,
                "duedate":compliance_record.duedate,
                "function":compliance_record.function,
                "issubscribed": issubscribed_value,
                "isinsubscription": isinsubscription_value,
            }
        )
    return result_list
