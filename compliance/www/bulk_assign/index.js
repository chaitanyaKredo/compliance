frappe.ready(function () {
    let complianceData = [];
    let  users = [];
    let  changesList = [];
    frappe.call({
	method:'compliance.client.get_dependent_doctypes',
	args:{doc1:'User',doc2:'Compliancetracker'},
	callback: function(response){
		if(response.message){
			complianceData = response.message.Compliancetracker;
			users = response.message.User;
			const complianceNames = complianceData.map(item => item.name);
    			populateTableWithComplianceNames(complianceNames,complianceData,users,changesList)
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

function populateTableWithComplianceNames(complianceNames,complianceData,userList,changesList) {
    const tableBody = document.querySelector('#complianceTable tbody');
    complianceNames.forEach(name => {
        const row = tableBody.insertRow();
        const cell1 = row.insertCell(0);
        cell1.textContent = name;
        const cell2 = row.insertCell(1);
        const userDropdown = createUserDropdown();
        cell2.appendChild(userDropdown);
        userDropdown.addEventListener('change', function () {
            trackChanges(name, userDropdown.value, complianceData,userList,changesList);
        });
    });
}

function createUserDropdown() {
    const dropdown = document.createElement('select');
    dropdown.className = 'form-control';
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
    const compliance = complianceData.find(item => item.name === complianceName);
    const selectedUserObj =  userList.find(item => item.full_name === selectedUser);
    const  payload =  createPayload(compliance,selectedUserObj);
    changesList.push(payload);
}

function makePostRequest(payload) {
    frappe.call({
		method:'compliance.client.update_or_create_records',
		type:'POST',
		args:{docname:'Complianceassignment',docdata_list:payload},
		callback:function(response){
			console.log(response.message);
		}
	})
}

function createPayload(compliance,selectedUser) {
    return {
	    "assignedto":selectedUser.name,
	    "compliance":compliance.name,
	    "supervisor":'compliancesupervisor@kredo.in',
	    'startdate':compliance.startdate,
	    'duedate':compliance.duedate,
	    'status':'Not Started',
	    'ispublic':true};
}
