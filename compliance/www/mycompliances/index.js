frappe.ready(function () {
  const currentUser = frappe.session.user;

  frappe.call({
    method: 'frappe.client.get_list',
    args: {
      doctype: 'Complianceassignment',
      fields: ['*'],
    },
    callback: function (response) {
      if (response.message) {
        const items = response.message;
        const userItems = items.filter(item => item.assignedto === currentUser);

        generateTable(userItems);
      }
    },
  });

  function generateTable(filteredItems) {
    const tableContainer = document.getElementById('table-container');
    const table = document.createElement('table');
    table.className = 'table';

    const headers = ['Compliance', 'Start Date', 'Due Date'];
    const headerRow = table.insertRow();
    headers.forEach(headerText => {
      const th = document.createElement('th');
      th.textContent = headerText;
      headerRow.appendChild(th);
    });

    filteredItems.forEach(item => {
      const row = table.insertRow();
      row.setAttribute('data-item-id', item.name);
      row.classList.add('item-row');
      const cell1 = row.insertCell(0);
      cell1.textContent = item.compliance;
      const cell2 = row.insertCell(1);
      cell2.textContent = item.startdate;
      const cell3 = row.insertCell(2);
      cell3.textContent = item.duedate;
    });

    const itemRows = document.querySelectorAll('.item-row');
    itemRows.forEach(itemRow => {
      itemRow.addEventListener('mouseenter', function () {
        itemRow.style.cursor = 'pointer';
        itemRow.style.backgroundColor = '#7FFFD4';
      });

      itemRow.addEventListener('mouseleave', function () {
        itemRow.style.backgroundColor = '';
      });
    });


    table.addEventListener('click', function (event) {
      const clickedRow = event.target.closest('.item-row');
      if (clickedRow) {
        const itemId = clickedRow.getAttribute('data-item-id');
        if (itemId) {
          const selectedItem = filteredItems.find(item => item.name === itemId);
          if (selectedItem) {
            displayItemDetails(selectedItem);
          }
        }
      }
    });

    tableContainer.appendChild(table);
  }

  function displayItemDetails(item) {
    const itemDetailsDiv = document.getElementById('item-details');
    itemDetailsDiv.innerHTML = `
      <div class="item-card">
        <h2>${item.compliance}</h2>
        <p>Start Date: ${item.startdate}</p>
        <p>Due Date: ${item.duedate}</p>
      </div>
    `;
  }
});
