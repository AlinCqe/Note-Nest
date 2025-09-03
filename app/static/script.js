    document.addEventListener('DOMContentLoaded', function(e) {
        e.preventDefault();
        const container = document.getElementById('sheets-container');
        const searchForm = document.getElementById('search-form'); // navbar search form
        const filterForm = document.getElementById('filter-form');

        const author_filters = document.getElementById('author-filters');
        const author_checkboxes = author_filters.querySelector('.checkboxes');

        const instrument_filters = document.getElementById('instrument-filters');
        const instrument_checkboxes = instrument_filters.querySelector('.checkboxes');

        const category_filters = document.getElementById('category-filters');
        const category_checkboxes = category_filters.querySelector('.checkboxes');

        if (!container || !searchForm) return;

        function renderCheckboxs(data){

            author_checkboxes.innerHTML = ''
            instrument_checkboxes.innerHTML = ''
            category_checkboxes.innerHTML = ''

            data.instruments.forEach(instrument => {
                const wraper = document.createElement('div');

                const checkbox = document.createElement('input');
                checkbox.type="checkbox";
                checkbox.value=instrument;
                checkbox.name="instruments"

                const label = document.createElement('label');
                label.textContent = instrument;

                wraper.appendChild(checkbox)
                wraper.appendChild(label)

                instrument_checkboxes.appendChild(wraper)
            })
            
            data.categories.forEach(category => {
                const wraper = document.createElement('div');

                const checkbox = document.createElement('input');
                checkbox.type="checkbox";
                checkbox.value=category;
                checkbox.name="categories"

                const label = document.createElement('label');
                label.textContent = category;

                wraper.appendChild(checkbox)
                wraper.appendChild(label)

                category_checkboxes.appendChild(wraper)
            })

            data.authors.forEach(author => {
                const wraper = document.createElement('div');

                const checkbox = document.createElement('input');
                checkbox.type="checkbox";
                checkbox.value=author;
                checkbox.name="authors"

                const label = document.createElement('label');
                label.textContent = author;

                wraper.appendChild(checkbox)
                wraper.appendChild(label)

                author_checkboxes.appendChild(wraper)
            })
        }

        function renderSheets(data) {
            container.innerHTML = ''; // clear previous results
            data.forEach(sheet => {
                const col = document.createElement('div');
                col.classList.add('col-sm-6', 'col-md-4', 'mb-4');

                const link = document.createElement('a');
                console.log(sheet.safe_filename )
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
                container.appendChild(col);
            });
        }

        // Initial load: fetch all sheets
        fetch('/get_sheets')

            .then(res => res.json())
            .then(data => {
                console.log(data);
                renderCheckboxs(data.filters)
                renderSheets(data.sheets);});

        // Handle search + filters
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(searchForm);
            const q = formData.get('q') || '';

            const second_formData = new FormData(filterForm);

            // Gather checked filters
            const authors = second_formData.getAll('authors').join(',');
            const categories = second_formData.getAll('categories').join(',');
            const instruments = second_formData.getAll('instruments').join(',');
            console.log(instruments, "asdsad")
            // Build query params
            const params = new URLSearchParams();
            if (q) params.append('q', q);
            if (authors) params.append('authors', authors);
            if (categories) params.append('categories', categories);
            if (instruments) params.append('instruments', instruments);
            console.log(params)
            fetch(`/get_sheets?${params.toString()}`)
                .then(res => res.json())
                .then(data => {renderSheets(data.sheets);
                            renderCheckboxs(data.filters);}
            );
        });
    });
