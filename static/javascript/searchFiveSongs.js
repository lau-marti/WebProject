let accessToken; // Variable global para almacenar el token de acceso

    // Función para obtener el token de acceso de la API de Spotify
    function obtenerToken(callback) {
        $.ajax({
            url: 'https://accounts.spotify.com/api/token',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + btoa('7f44fa05891c4b0388022a3317aea4cb:d9e691dd766a45509a5f4f9b8ce026c6')
            },
            data: 'grant_type=client_credentials',
            success: function(response) {
                accessToken = response.access_token; // Almacenar el token de acceso en la variable global
                callback();
            },
            error: function(xhr, status, error) {
                console.error("Error al obtener el token de acceso:", error);
            }
        });
    }

    // Función para realizar la búsqueda de canciones
    function buscarCancion() {
        const nombreCancion = $('#searchInput').val();
        obtenerToken(function() {
            $.ajax({
                url: `https://api.spotify.com/v1/search?q=${encodeURIComponent('track:' + nombreCancion)}&type=track`,
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + accessToken
                },
                success: function(response) {
                    obtenerInfoArtistas(response.tracks.items);
                },
                error: function(xhr, status, error) {
                    console.error("Error al buscar la canción:", error);
                }
            });
        });
    }

    // Función para obtener información de los artistas de las pistas
    function obtenerInfoArtistas(items) {
        const artistasPromises = [];

        // Recorrer las pistas y obtener información de los artistas
        items.forEach(function(item) {
            const artistasIds = item.artists.map(artist => artist.id);
            artistasIds.forEach(function(artistId) {
                const promise = $.ajax({
                    url: `https://api.spotify.com/v1/artists/${artistId}`,
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + accessToken
                    }
                });
                artistasPromises.push(promise);
            });
        });

        // Esperar a que todas las solicitudes a la API de artistas se completen
        Promise.all(artistasPromises)
            .then(function(artistasInfo) {
                displayResults(items, artistasInfo);
            })
            .catch(function(error) {
                console.error("Error al obtener la información de los artistas:", error);
            });
    }

    // Función para agregar una canción a la base de datos
    function agregarCancion(nombreCancion, nombreArtista, nombreAlbum) {
        // Crear un objeto FormData y agregar los datos
        const formData = new FormData();
        formData.append('nombre_cancion', nombreCancion);
        formData.append('nombre_artista', nombreArtista);
        formData.append('nombre_album', nombreAlbum);

        // Obtener el token CSRF de la cookie
        const csrftoken = getCookie('csrftoken');

        // Enviar la solicitud AJAX con fetch
        fetch('add_song', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al agregar la canción');
            }
            console.log('Canción agregada correctamente');
            return response.json();
        })
        .catch(error => console.error('ERROR:', error));
    }

    // Función para obtener el valor de una cookie por su nombre
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

    // Función para mostrar los resultados de la búsqueda
    function displayResults(items, artistasInfo) {
        const searchResults = $('#searchResults');
        searchResults.empty(); // Limpiar resultados anteriores

        // Recorrer las pistas y mostrar la información
        items.forEach(function(item, index) {
            const resultDiv = $('<div>');
            const duracion = formatDuracion(item.duration_ms); // Obtener la duración formateada

            resultDiv.html(`
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <h1>Canción ${index + 1}:</h1>
                    <h2 style="color: white">Titulo: ${item.name}</h2>
                    <p>Artista(s): ${item.artists.map((artist, artistIndex) => artist.name + " (" + artistasInfo[index * item.artists.length + artistIndex].genres.join(", ") + ")").join(", ")}</p>
                    <p>Álbum: ${item.album.name}</p>
                    <p>URL del álbum: <a href="${item.album.external_urls.spotify}" target="_blank">${item.album.external_urls.spotify}</a></p>
                    <img src="${item.album.images[0].url}" alt="Album Image" style="max-width: 200px; max-height: 200px;"></p>
                    <p>Duración: ${duracion}</p>
                    <button class="genericButton" onclick="agregarCancion('${item.name}', '${item.artists[0].name}', '${item.album.name}')">Add</button>
                    <hr style="border-top: 1px solid white;">  <!-- Línea blanca de separación -->
                </div>
            `);
            searchResults.append(resultDiv);
        });
    }

    // Función para formatear la duración de milisegundos a formato de minutos y segundos
    function formatDuracion(duracion_ms) {
        const duracionSegundos = Math.floor(duracion_ms / 1000);
        const minutos = Math.floor(duracionSegundos / 60);
        const segundos = duracionSegundos % 60;
        return `${minutos}:${segundos < 10 ? '0' : ''}${segundos}`;
    }