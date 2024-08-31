// gallery/static/gallery/favorites.js

function addToFavorites(photo_id, album_id) {
    const data = {photo_id: photo_id, album_id: album_id};

    fetch('/api/favorites/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (response.ok) {
            document.getElementById('favorite-buttons').innerHTML =
                `<button id="remove-favorite-btn" onclick="removeFromFavorites(${photo_id}, ${album_id})">Удалить из избранного</button>`;
        } else {
            console.error('Error adding to favorites:', response.statusText);
        }
    })
    .catch(error => console.error('Fetch error:', error));
}

function removeFromFavorites(photo_id, album_id) {
    const data = {photo_id: photo_id, album_id: album_id};

    fetch('/api/favorites/remove/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (response.ok) {
            document.getElementById('favorite-buttons').innerHTML =
                `<button id="add-favorite-btn" onclick="addToFavorites(${photo_id}, ${album_id})">Добавить в избранное</button>`;
        } else {
            console.error('Error removing from favorites:', response.statusText);
        }
    })
    .catch(error => console.error('Fetch error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
