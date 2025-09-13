document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById("upload-sheet-form");

    console.log("upload_sheet.js loaded!");
    if (!form) {
        console.log('asdsadsad')
        return; // safety check
    }
    form.addEventListener("submit", function(e) {   
        e.preventDefault();

        var formData = new FormData(form);

        fetch("/upload_file", {
            method: "POST",
            body: formData
        })
        .then(function(response) {
            if (!response.ok) {
                // if backend sends 400 or redirect to login, throw
                throw new Error("Server error: " + response.status);
            }
            return response.json();
        })
        .then(function(data) {
            if (data.success) {
                alert(data.message || "File uploaded successfully!");

                // Close modal
                var modalEl = document.getElementById("uploadSheetModal");
                var modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();

                // Reset form
                form.reset();
            } else {
                alert("Error uploading file: " + (data.message || "Unknown error"));
            }
        })
        .catch(function(error) {
            alert("Error uploading file: " + error.message);
        });
    });
});
