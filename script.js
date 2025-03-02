document.addEventListener('DOMContentLoaded', () => {
    // Format revenue
    function formatRevenue(num) {
        return '$' + Number(num).toLocaleString();
    }

    // Clean references
    function cleanText(str) {
        return str.replace(/[\[\]\d]/g, '');
    }

    // Fetch data
    fetch('public/films.json')
        .then(response => response.json())
        .then(films => {
            const tbody = document.getElementById('films-tbody');
            films.forEach(film => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${film.title}</td>
                    <td>${film.year}</td>
                    <td>${cleanText(film.country)}</td>
                    <td>${cleanText(film.director)}</td>
                    <td>${formatRevenue(film.revenue)}</td>
                `;
                tbody.appendChild(row);
            });

            // Add search functionality
            const searchInput = document.getElementById('searchInput');
            searchInput.addEventListener('input', () => {
                const filter = searchInput.value.toLowerCase();
                const rows = tbody.querySelectorAll('tr');
                rows.forEach(row => {
                    // Check if row’s text matches the query
                    row.style.display = row.textContent.toLowerCase().includes(filter) ? '' : 'none';
                });
            });
        })
        .catch(console.error);
});