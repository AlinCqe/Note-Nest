document.addEventListener('DOMContentLoaded', function() {
  const container = document.getElementById('sheets-container');
  const searchForm = document.getElementById('search-form');
  
  // Get the checkbox container elements
  const author_filters = document.getElementById('author-filters');
  const author_checkboxesContainer = author_filters.querySelector('.checkboxes');
  const instrument_filters = document.getElementById('instrument-filters');
  const instrument_checkboxesContainer = instrument_filters.querySelector('.checkboxes');
  const category_filters = document.getElementById('category-filters');
  const category_checkboxesContainer = category_filters.querySelector('.checkboxes');

  if (!container || !searchForm) return;

  // Utility function to parse query parameters from URL
  function getQueryParams() {
    return new URLSearchParams(window.location.search);
  }

  // Render available filter checkboxes and mark those that were checked
  function renderCheckboxes(filtersData) {
    // Clear previous content
    author_checkboxesContainer.innerHTML = '';
    instrument_checkboxesContainer.innerHTML = '';
    category_checkboxesContainer.innerHTML = '';

    // Get the current query values for each filter
    const currentParams = getQueryParams();
    const selectedAuthors = currentParams.getAll('authors');
    const selectedInstruments = currentParams.getAll('instruments');
    const selectedCategories = currentParams.getAll('categories');

    // Render instrument checkboxes
    filtersData.instruments.forEach(instrument => {
      const wrapper = document.createElement('div');
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.name = 'instruments';
      checkbox.value = instrument;
      if (selectedInstruments.includes(instrument)) {
        checkbox.checked = true;
      }
      // Add listener to re-query on change
      checkbox.addEventListener('change', handleFilterChange);
      const label = document.createElement('label');
      label.textContent = instrument;
      wrapper.appendChild(checkbox);
      wrapper.appendChild(label);
      instrument_checkboxesContainer.appendChild(wrapper);
    });

    // Render category checkboxes
    filtersData.categories.forEach(category => {
      const wrapper = document.createElement('div');
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.name = 'categories';
      checkbox.value = category;
      if (selectedCategories.includes(category)) {
        checkbox.checked = true;
      }
      checkbox.addEventListener('change', handleFilterChange);
      const label = document.createElement('label');
      label.textContent = category;
      wrapper.appendChild(checkbox);
      wrapper.appendChild(label);
      category_checkboxesContainer.appendChild(wrapper);
    });

    // Render author checkboxes
    filtersData.authors.forEach(author => {
      const wrapper = document.createElement('div');
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.name = 'authors';
      checkbox.value = author;
      if (selectedAuthors.includes(author)) {
        checkbox.checked = true;
      }
      checkbox.addEventListener('change', handleFilterChange);
      const label = document.createElement('label');
      label.textContent = author;
      wrapper.appendChild(checkbox);
      wrapper.appendChild(label);
      author_checkboxesContainer.appendChild(wrapper);
    });
  }

  function renderSheets(data) {
    container.innerHTML = ''; // clear previous results
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
      categories.textContent = sheet.categories;
      body.appendChild(categories);

      const instruments = document.createElement('p');
      instruments.textContent = sheet.instruments;
      body.appendChild(instruments);

      const userDiv = document.createElement('div');
      userDiv.classList.add('row');

      const photo = document.createElement('img');
      photo.src = `/static/profile_pictures/${sheet.profile_picture}`;
      photo.alt = 'Profile Picture';
      photo.classList.add('col-md-3');
      userDiv.appendChild(photo);

      const username = document.createElement('p');
      username.textContent = sheet.username;
      username.classList.add('col-md-9');
      userDiv.appendChild(username);

      body.appendChild(userDiv);
      card.appendChild(body);
      link.appendChild(card);
      col.appendChild(link);
      container.appendChild(col);
    });
  }

  // Fetch sheets from the backend using the query parameters from the URL
  function fetchSheets() {
    const queryParams = getQueryParams();
    let fetchUrl = '/get_sheets';
    const qs = queryParams.toString();
    if (qs) {
      fetchUrl += '?' + qs;
    }
    fetch(fetchUrl)
      .then(res => res.json())
      .then(data => {
        // Expected structure: { sheets: [...], filters: { authors: [...], instruments: [...], categories: [...] } }
        renderCheckboxes(data.filters);
        renderSheets(data.sheets);
      })
      .catch(err => console.error("Error fetching sheets:", err));
  }

  // Handler for filter change events (called whenever a checkbox is toggled)
  function handleFilterChange() {
    const params = new URLSearchParams();

    // Also capture search text if available
    const formData = new FormData(searchForm);
    const q = formData.get('q');
    if (q) {
      params.append('q', q);
    }

    // Gather selected checkboxes from each filter group
    const instrumentChecked = Array.from(document.querySelectorAll('input[name="instruments"]:checked')).map(el => el.value);
    instrumentChecked.forEach(value => params.append('instruments', value));

    const categoryChecked = Array.from(document.querySelectorAll('input[name="categories"]:checked')).map(el => el.value);
    categoryChecked.forEach(value => params.append('categories', value));

    const authorChecked = Array.from(document.querySelectorAll('input[name="authors"]:checked')).map(el => el.value);
    authorChecked.forEach(value => params.append('authors', value));

    // Update the browser URL without reloading the page
    history.pushState(null, '', '/?' + params.toString());
    // Fetch the updated sheets based on current filters
    fetchSheets();
  }

  // Initial data load
  fetchSheets();

  // Handle search (text) form submission
  searchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    // For search form submission, we read all filters along with the search text.
    handleFilterChange(); // This will update the URL and fetch data.
  });
});