document.addEventListener('DOMContentLoaded', () => {
    // Format revenue for better display quality
    function formatRevenue(num) {
        return '$' + Number(num).toLocaleString();
    }

    // Some entries in data have wikipedia references like '[1]',
    // so we need to remove them to display the data properly
    function cleanText(str) {
        return str.replace(/[\[\]\d]/g, '');
    }

    // Fetch films data from JSON file
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
        })
        .catch(console.error);
});