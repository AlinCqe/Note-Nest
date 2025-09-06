document.addEventListener("DOMContentLoaded", function(e){

    const user_container = document.getElementById("user-container");
    const sheets_container = document.getElementById("sheets-container");


    const user_id = user_container.dataset.userId;
    console.log(user_id);

    user_container.innerHTML = '';
    sheets_container.innerHTML = '';

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

            const categories = document.createElement('p');
            categories.classList.add('card-categories');
            categories.textContent = sheet.categories;
            body.appendChild(categories);

            const instruments = document.createElement('p');
            instruments.classList.add('card-instruments');
            instruments.textContent = sheet.instruments;
            body.appendChild(instruments);

            card.appendChild(body);
            link.appendChild(card);
            col.appendChild(link);
            sheets_container.appendChild(col);
        });
    }

    function renderUserData(data){
        user_container.innerHTML = ''
            
        const photo = document.createElement('img');   // use img tag
        photo.src = `/static/profile_pictures/${data.profile_picture}`;

        photo.alt = 'Profile Picture';

        user_container.appendChild(photo)

        const username = document.createElement('h1');
        username.textContent = data.username

        user_container.appendChild(username)
    }

    fetch(`/api/user/${user_id}`)
        .then(res => res.json())
        .then(data => {
            renderSheets(data.sheets)
            renderUserData(data.user_data[0])
        })


})