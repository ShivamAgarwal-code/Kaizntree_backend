function showSuccessMessage(message) {   
    $('.alert-success').removeClass('d-none').addClass('show');  
} 

function showErrorMessage(message) {    
    $('.alert-warning').removeClass('d-none').addClass('show');
}

function create_category(){
    
    const apiUrl = 'http://localhost:8000/api/v1/items/category/add/';
    const authToken = '514b1ac473ce9d7054cd8b032109efc3d19b74ee';

    var categoryName = document.getElementById('categoryName').value;

    const requestData = {
        name: categoryName,
    };

    fetch(apiUrl, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${authToken}`,
    },
    body: JSON.stringify(requestData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Show success message
        showSuccessMessage();  
    })
    .catch(error => {
        console.error('Error:', error);
        // Show error message
        showErrorMessage();
    });
}

function create_item(){

    var itemName = document.getElementById('itemName').value;
    var category = document.getElementById('category').value;
    var sku = document.getElementById('sku').value;
    var tag = document.getElementById('tag').value;
    var currentStock = document.getElementById('currentStock').value;
    var availableStock = document.getElementById('availableStock').value;
    var status = document.getElementById('status').value;

    const apiUrl = 'http://localhost:8000/api/v1/items/add/';
    const authToken = '514b1ac473ce9d7054cd8b032109efc3d19b74ee';

    // Define parameters
    const params = {
        name: itemName,
        category: category,
        sku: sku,
        tag: tag,
        currentStock: currentStock,
        availableStock: availableStock,
        status: status
    };

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${authToken}`
        },
        body: JSON.stringify(params),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            showErrorMessage()
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        showSuccessMessage();
        // Handle success
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage()
        // Handle error
    });
}
