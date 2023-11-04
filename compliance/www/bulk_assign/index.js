frappe.ready(function () {
    let complianceData = [];
    let  users = [];
    let  changesList = [];
   frappe.call({
	method:'compliance.client.get_dependent_doctypes',
	args:{doc1:'User',doc2:'Complianceassignment',filters_doc1:{},filters_doc2:{"assignedto": ["=", ""]}},
	callback: function(response){
		if(response.message){
			complianceData = response.message.Complianceassignment;
			users = response.message.User;
    			populateTableWithComplianceNames(complianceData,users,changesList)
    			const userNames = users.map(item => item.full_name);
    			populateDropdownsInTable(userNames);
		}
	},
	});
    const saveButton = document.querySelector('#saveButton');
    saveButton.addEventListener('click', function () {
        makePostRequest(changesList);
    });
});

function populateTableWithComplianceNames(complianceData,userList,changesList) {
    const tableBody = document.querySelector('#complianceTable tbody');
    complianceData.forEach(compliance => {
        const row = tableBody.insertRow();
        const cell1 = row.insertCell(0);
        cell1.textContent = compliance.route;
        const cell2 = row.insertCell(1);
	cell2.textContent = compliance.duedate
	const cell3 = row.insertCell(2);
        const userDropdown = createUserDropdown();
        cell3.appendChild(userDropdown);
        userDropdown.addEventListener('change', function () {
            trackChanges(compliance.route, userDropdown.value, complianceData,userList,changesList);
        });
    });
}

function createUserDropdown() {
    const dropdown = document.createElement('select');
    dropdown.className = 'form-control  form-select form-select-sm';
    return dropdown;
}

function populateDropdownsInTable(userNames) {
    const dropdowns = document.querySelectorAll('#complianceTable select');
    dropdowns.forEach(dropdown => {
        userNames.forEach(userName => {
            const option = document.createElement('option');
            option.value = userName;
            option.textContent = userName;
            dropdown.appendChild(option);
        });
    });
}

function trackChanges(complianceName, selectedUser, complianceData,userList,changesList) {
    const compliance = complianceData.find(item => item.route === complianceName);
    const selectedUserObj =  userList.find(item => item.full_name === selectedUser);
    const  payload =  createPayload(compliance,selectedUserObj);
    changesList.push(payload);
}

function makePostRequest(payload) {
    frappe.call({
		method:'compliance.client.update_or_create_records',
		type:'PUT',
		args:{docname:'Complianceassignment',docdata_list:payload},
		callback:function(response){
			console.log(response.message);
			frappe.show_alert({message:__('Updated Sucessfully'),indicator:'green'}, 5);
		}
	})
}

function createPayload(compliance,selectedUser) {
    return {
	    "assignedto":selectedUser.name,
	    "name":compliance.name,
	    "supervisor":'compliancesupervisor@kredo.in',
	    'ispublic':true
	   };
}
