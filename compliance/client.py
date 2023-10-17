import frappe
import json

@frappe.whitelist()
def get_dependent_doctypes(doc1,doc2):
	doc1_list = frappe.get_all(doc1,fields=['*'])
	doc2_list = frappe.get_all(doc2,fields=['*'])
	return {doc1:doc1_list,doc2:doc2_list}

@frappe.whitelist(methods=["POST", "PUT"])
def update_or_create_records(docname, docdata_list):
    docdata_list = json.loads(docdata_list)
    created_or_updated_records = []
    for docdata in docdata_list:
        print(docdata)
        existing_record = frappe.get_all(docname, filters={'compliance':docdata.compliance})
        print(existing_record)
        if existing_record:
            doc = frappe.get_doc(docname, existing_record[0].name)
            doc.update(docdata)
            doc.save()
            created_or_updated_records.append(doc.name)
        else:
            doc = frappe.new_doc(docname)
            doc.update(docdata)
            doc.insert()
            created_or_updated_records.append(doc.name)
    frappe.db.commit()
    return created_or_updated_records
