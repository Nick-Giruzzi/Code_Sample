(function () {
    //var listCont = document.getElementById('listContainer');
    x = setInterval(function () {
        var xhr = new XMLHttpRequest();
        xhr.open('GET',`http://10.3.3.11/op_code_handler`,true);
        xhr.onerror = err => console.log('error: ' + err.message); //window.location.replace("http://vault.merch.codes/logout") & 
        xhr.onload = function () {
            if (this.readyState == 4 && this.status == 200) {
                data = JSON.parse(this.responseText);
                var current_codes = data['stored_codes']
                if (current_codes.length === 0 ) {
                    //document.getElementById('stored_codes').textContent = '';  
                    document.getElementById('listContainer').textContent = '';
                }
                else {
                    document.getElementById('listContainer').textContent = '';
                    //document.getElementById('stored_codes').innerHTML = "Stored Codes: " +current_codes;  
                    current_codes.forEach(element => {
                        const listItem = document.createElement('div');
                        listItem.textContent = element;
                        listItem.className = 'list-item';
                        document.getElementById('listContainer').appendChild(listItem);
                    });                    
                }           
            }
        }
        xhr.send();
    }, 1000);
})();
