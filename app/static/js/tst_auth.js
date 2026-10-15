document.addEventListener('DOMContentLoaded', function() {
    const accounts = [
        { type: 'Savings', number: '123456789', balance: '$1,500.00' },
        { type: 'Checking', number: '987654321', balance: '$2,300.00' },
        { type: 'Credit Card', number: '**** **** **** 1234', balance: '$500.00' }
    ];

    const tableBody = document.querySelector('#account-table tbody');

    accounts.forEach(account => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${account.type}</td>
            <td>${account.number}</td>
            <td>${account.balance}</td>
        `;
        tableBody.appendChild(row);
    });
});