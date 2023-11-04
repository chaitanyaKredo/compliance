frappe.ready(function () {
    let complianceData = [];
    const selectedRows = [];
    let users = [];
    const options = {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric",
    };
    frappe.call({
        method: 'compliance.client.get_dependent_doctypes',
        args: { doc1: 'User', doc2: 'Complianceassignment', filters_doc1: {}, filters_doc2: { "assignedto": ["=", ""] } },
        callback: function (response) {
            if (response.message) {
                complianceData = response.message.Complianceassignment;
                users = response.message.User;
		const dropdown = document.createElement('select');
		dropdown.className = 'form-control  form-select form-select-sm';
		users.forEach(user => {
    			const option = document.createElement('option');
    			option.value = user.name;
    			option.text = user.full_name;
    			dropdown.appendChild(option);
			});
                const tableEl = document.getElementById('table-container');
                const datatable = new DataTable(tableEl, {
                    columns: ['Compliance Name', 'Due Date','Assigned To'],
                    data: complianceData.map(data => [data.route, data.duedate,dropdown]),
                    checkboxColumn: true,
                    inlineFilters: true,
                    layout: "fluid"
                });
                tableEl.addEventListener("change", function (e) {
		   console.log(datatable);
                    if (e.target.type === "checkbox") {
                        const row = e.target.closest("tr");
                        const rowIndex = datatable.row(row).index();
			const rowData = complainceData[rowIndex];
                        if (e.target.checked) {
                            const rowData = { ...complianceData[rowIndex] };
                            selectedRows.push({ index: rowIndex, data: rowData });
                        } else {
                            const index = selectedRows.findIndex((selectedRow) => selectedRow.index === rowIndex);
                            if (index > -1) {
                                selectedRows.splice(index, 1);
                            }
                        }
                        console.log("Selected Rows: ", selectedRows);
                    }
                });
            }
        }
    });
});
