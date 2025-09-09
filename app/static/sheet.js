document.addEventListener('DOMContentLoaded', function(e){
    e.preventDefault();
    const sheet_container = document.getElementById('sheet-page');
    const safe_filename = sheet_container.dataset.sheet;

    fetch(`/api/sheet/${safe_filename}`)
        .then(res => res.json())
        .then(data =>{
            const pdf_container = document.getElementById("pdf-container")
            const sheet_data_container = document.getElementById("sheet-data-container")
            sheet_data_container.innerHTML = '';
            pdf_container.innerHTML = '';

            const sheets = data.sheets
            const sheet = sheets[0]

            const embed = document.createElement('embed');
            console.log(sheet.safe_filename)
            embed.src = `/static/uploads/${sheet.safe_filename}#page=1&zoom=50`;
            embed.type = 'application/pdf';
            embed.classList.add('card-img-top');
            embed.style.width = '100%'; 
            embed.style.height = '400px';
            pdf_container.appendChild(embed);

            console.log(sheet.instruments)
            const song_name = document.createElement('h1')
            song_name.textContent = `Song name: ${sheet.song_name}`
            sheet_data_container.appendChild(song_name)

            const authors = document.createElement('h2')
            authors.textContent = `Authors: ${sheet.authors.join(', ')}`;
            sheet_data_container.appendChild(authors)

            const instruments = document.createElement('h2')
            instruments.textContent = `Instruments: ${sheet.instruments.join(', ')}`
            sheet_data_container.appendChild(instruments)

            const categories = document.createElement('h2')
            categories.textContent = `Categories: ${sheet.categories.join(' ,')}`
            sheet_data_container.appendChild(categories)

            user_container = document.createElement('div')
            user_container.innerHTML = '';
                
            const photo = document.createElement('img');   
            photo.src = `/static/profile_pictures/${sheet.profile_picture}`;
            photo.alt = 'Profile Picture';
            photo.style.cursor = "pointer"; // make it look clickable

            user_container.appendChild(photo);

            const username = document.createElement('h1');
            username.textContent = sheet.username;
            user_container.appendChild(username);
        
            sheet_data_container.appendChild(user_container)
        })
})