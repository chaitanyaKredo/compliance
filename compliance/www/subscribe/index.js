frappe.ready(function () {
  frappe.call({
        method:'compliance.client.get_subscribed_doctype_list',
        args:{
		doctype: 'Compliancetracker',
      		fields: ['*'],
	},
        callback: function(response){
                if(response.message){
                        complianceData = response.message;
			const headers = ["Compliance", "Due Date","Function", "Subscribed"];
			create_table_with_check_boxes(headers,complianceData);
                        console.log(complianceData)
                }
        },
        });
function makePostRequest(compliance,isSubscribed){
    const payload = {name:compliance.name,is_in_list:compliance.isinsubscription,is_subscribed:isSubscribed};
    frappe.call({
                method:'compliance.client.update_or_create_subscription',
                type:'PUT',
                args:{docname:'Subscription',payload},
                callback:function(response){
                        frappe.show_alert({message:__('Updated Sucessfully'),indicator:'green'}, 5);
                }
        })
}
function create_table_with_check_boxes(headers,data){
    var table = document.createElement("table");
    table.className = "table table-sm table-bordered";
    var thead = table.createTHead();
    thead.className = "thead-light";
    var headerRow = thead.insertRow();
    headers.forEach(function (header) {
        var th = document.createElement("th");
        th.scope = "col";
        th.appendChild(document.createTextNode(header));
        headerRow.appendChild(th);
    });
    var tbody = table.createTBody();
    data.forEach(function (compliance) {
        var row = tbody.insertRow();
        var complianceNameCell = row.insertCell(0);
        complianceNameCell.appendChild(
            document.createTextNode(compliance.name)
        );
        var dueDateCell = row.insertCell(1);
        dueDateCell.appendChild(document.createTextNode(compliance.duedate));
        var functionCell = row.insertCell(2);
        functionCell.appendChild(document.createTextNode(compliance.function));
        var isSubscribedCell = row.insertCell(3);
        var checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = compliance.issubscribed;
        isSubscribedCell.appendChild(checkbox);
        checkbox.addEventListener('change',function(){
              makePostRequest(compliance,this.checked);
        });
    });
    const tableContainer = document.getElementById("table-container");
    tableContainer.appendChild(table)
}
});
