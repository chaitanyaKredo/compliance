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
