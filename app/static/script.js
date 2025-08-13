document.addEventListener('DOMContentLoaded', function(e){

    fetch('/get_sheets')
        
    .then(response => response.json())
    .then(data => {console.log(data); // This will show the data in the console// 
        });
    })