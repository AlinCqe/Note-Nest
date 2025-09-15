document.addEventListener("DOMContentLoaded", function() {

    const user_container = document.getElementById("user-container");
    const sheets_container = document.getElementById("sheets-container");

    const user_id = user_container.dataset.userId;

    user_container.innerHTML = '';
    sheets_container.innerHTML = '';

    // -------------------
    // Render sheets cards
    // -------------------
    function renderSheets(data) {
        sheets_container.innerHTML = ''; 
        data.forEach(sheet => {
            const col = document.createElement('div');
            col.classList.add('col-sm-6', 'col-md-4', 'mb-4');

            const link = document.createElement('a');
            link.href = `/sheet/${sheet.safe_filename}`;
            link.style.textDecoration = 'none';

            const card = document.createElement('div');
            card.classList.add('card', 'shadow-sm');

            const embed = document.createElement('embed');
            embed.src = `/static/uploads/${sheet.safe_filename}#page=1&zoom=50`;
            embed.type = 'application/pdf';
            embed.classList.add('card-img-top');
            embed.style.width = '100%';
            embed.style.height = '200px';
            card.appendChild(embed);

            const body = document.createElement('div');
            body.classList.add('card-body');

            const title = document.createElement('h5');
            title.classList.add('card-title');
            title.textContent = sheet.song_name;
            body.appendChild(title);

            const authors = document.createElement('p');
            authors.classList.add('card-authors');
            authors.textContent = sheet.authors;
            console.log(sheet.authors)
            console.log('------------------')
            body.appendChild(authors);

            const categories = document.createElement('p');
            categories.classList.add('card-categories');
            categories.textContent = sheet.categories;

            body.appendChild(categories);

            const instruments = document.createElement('p');
            instruments.classList.add('card-instruments');
            instruments.textContent = sheet.instruments;
            body.appendChild(instruments);

            const editBtn = document.createElement('button');
            editBtn.classList.add('btn', 'btn-sm', 'btn-primary');
            editBtn.textContent = 'Edit';
            editBtn.setAttribute('data-bs-toggle', 'modal');
            editBtn.setAttribute('data-bs-target', '#editSheetModal');

            editBtn.addEventListener('click', function(event) {
                    event.stopPropagation(); 
                    event.preventDefault(); 

                document.getElementById('editSafeFilename').value = sheet.safe_filename;
                document.getElementById('editSongName').value = sheet.song_name;
                document.getElementById('editAuthors').value = sheet.authors.join(', ');
                document.getElementById('editCategories').value = sheet.categories.join(', ');
                document.getElementById('editInstruments').value = sheet.instruments.join(', ');
            });

            body.appendChild(editBtn);


            const deleteBtn = document.createElement('button');
            deleteBtn.classList.add('btn', 'btn-danger')
            deleteBtn.textContent = 'Delete'

            deleteBtn.setAttribute('data-bs-toggle', 'modal');
            deleteBtn.setAttribute('data-bs-target', '#deleteModal');
            deleteBtn.setAttribute('data-song-name', sheet.song_name);    
            deleteBtn.setAttribute('data-filename', sheet.safe_filename);

            deleteBtn.addEventListener('click', function(event) {
                event.stopPropagation();
                event.preventDefault();
            });


            body.appendChild(deleteBtn)

            card.appendChild(body);
            link.appendChild(card);
            col.appendChild(link);
            sheets_container.appendChild(col);



        });
    }

    // -------------------
    // Render user data
    // -------------------
    function renderUserData(data){
        user_container.innerHTML = '';
            
        const photo = document.createElement('img');   
        photo.src = `/static/profile_pictures/${data.profile_picture}`;
        photo.alt = 'Profile Picture';
        photo.style.cursor = "pointer";

        // If modal exists, make photo trigger it
        const modal = document.getElementById('profilePicModal');
        if (modal) {
            photo.setAttribute("data-bs-toggle", "modal");
            photo.setAttribute("data-bs-target", "#profilePicModal");
        }

        user_container.appendChild(photo);

        const username = document.createElement('h1');
        username.textContent = data.username;
        user_container.appendChild(username);
    }

    // -------------------
    // Fetch user + sheets data
    // -------------------
    fetch(`/api/user/${user_id}`)
        .then(res => res.json())
        .then(data => {
            renderSheets(data.sheets);
            renderUserData(data.user_data[0]);
        })
        .catch(err => console.error("Error fetching user data:", err));

    // -------------------
    // Handle profile picture upload
    // -------------------
    const change_photo_submit_button = document.getElementById('change_photo_submit_button');
    if (change_photo_submit_button) {
        change_photo_submit_button.addEventListener("click", function(e){
            e.preventDefault();

            const form = document.getElementById("profile-pic-form");
            const fileInput = form.querySelector('input[name="photo"]');
            const file = fileInput.files[0];

            if (!file) {
                alert("Please select a file");
                return;
            }

            const formData = new FormData();
            formData.append('photo', file);

            fetch(`/api/user/change_photo`, {
                method: 'PATCH', 
                body: formData
            })
            .then(res => res.json().then(data => ({status: res.status, ok: res.ok, body: data})))
            .then(result => {
                if (result.ok) {
                    location.reload();
                } else {
                    alert(result.body.error || "Upload failed");
                }
            })
            .catch(err => {
                console.error(err);
                alert("Upload failed");
            });
        });
    }


    // -------------------
    // Handle edit sheet
    // -------------------

    document.getElementById('editSheetForm').addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        console.log(formData)
        fetch('/api/edit_sheet', {
            method: 'PATCH',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
                
            } else {
                alert('Error: ' + data.message);
            }

           
            const modalEl = document.getElementById('editSheetModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
        })
        .catch(error => {
            alert('Error: ' + error);
        });
    });


    
    // -------------------
    // Handle delete sheet
    // -------------------
    let fileToDelete = "";

    const deleteModal = document.getElementById('deleteModal');

    deleteModal.addEventListener('show.bs.modal', function (event) {
        
        const button = event.relatedTarget;  
        fileToDelete = button.getAttribute('data-filename');
        const songName = button.getAttribute('data-song-name');
        document.getElementById('file-to-delete').textContent = songName;
    });

    // Handle delete confirmation
    document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
        fetch('/api/delete_sheet', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ safe_filename: fileToDelete })
        })
        .then(res => res.json())
        .then(data => {
        if (data.success) {
            alert("File deleted successfully!");
            location.reload(); // reload page or update UI
        } else {
            alert("Error: " + data.message);
        }
        })
        .catch(err => console.error(err));
    });


});
