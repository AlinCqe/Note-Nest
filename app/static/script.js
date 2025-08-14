document.addEventListener('DOMContentLoaded', function(e){

    fetch('/get_sheets')
        
    .then(response => response.json())
    .then(data => {console.log(data);  
        });
    })