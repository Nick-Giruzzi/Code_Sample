// Helper function to send POST request
function sendPostRequest(url, data) {
    fetch(url, {
        method: 'POST', // Method itself
        headers: {
            'Content-Type': 'application/json', // Indicates the content 
        },
        body: JSON.stringify(data) // Body data type must match "Content-Type" header
    })
    .then(response => response.json()) // Parses JSON response into native JavaScript objects
    .then(data => {
        //console.log(data); // Process success response
        //console.log(typeof data['Info'])
        //console.log(data['Info'])
        document.getElementById('msg').innerText = data['Info']

        if (data['Info'].includes("accepted") ) {
            window.location.href = "http://10.3.3.11/rebooting"
        }
    })
    .catch((error) => {
        console.log(response)
        console.log(data)
        console.error('Error:', error); // Handle error
    });
}