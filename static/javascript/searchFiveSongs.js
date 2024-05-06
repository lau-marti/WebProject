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

    // Función para mostrar los resultados de la búsqueda
    function displayResults(items, artistasInfo) {
        const searchResults = $('#searchResults');
        searchResults.empty(); // Limpiar resultados anteriores

        // Recorrer las pistas y mostrar la información
        items.forEach(function(item, index) {
            const resultDiv = $('<div>');
            resultDiv.html(`
                <p>Canción ${index + 1}:</p>
                <p>Nombre: ${item.name}</p>
                <p>Artista(s): ${item.artists.map((artist, artistIndex) => artist.name + " (" + artistasInfo[index * item.artists.length + artistIndex].genres.join(", ") + ")").join(", ")}</p>
                <p>Álbum: ${item.album.name}</p>
                <p>URL del álbum: <a href="${item.album.external_urls.spotify}" target="_blank">${item.album.external_urls.spotify}</a></p>
                <p>URL de la imagen del álbum: <img src="${item.album.images[0].url}" alt="Imagen del álbum"></p>
                <p>Duración: ${msToTime(item.duration_ms)}</p>
                <button onclick="agregarCancion('${item.name}', '${item.artists[0].name}', '${item.album.name}', '${item.album.images[0].url}', '${msToTime(item.duration_ms)}')">Add</button>
                <hr>
            `);
            searchResults.append(resultDiv);
        });
    }

    // Función auxiliar para convertir milisegundos a formato de tiempo
    function msToTime(duration) {
        let seconds = Math.floor((duration / 1000) % 60);
        let minutes = Math.floor((duration / (1000 * 60)) % 60);
        seconds = (seconds < 10) ? "0" + seconds : seconds;
        return minutes + ":" + seconds;
    }

    // Función para agregar una canción a la base de datos
    function agregarCancion(nombreCancion, nombreArtista, nombreAlbum, urlImagen, duracion, urlCancion) {
        // Obtener el playlist.id del campo oculto
        const urlcomponents = window.location.pathname.split('/')
        const playlistId = urlcomponents[3]

        // Crear un objeto FormData y agregar los datos
        const formData = new FormData();      // Ha modificar per afegir la resta de la info
        formData.append('nombre_cancion', nombreCancion);
        formData.append('nombre_artista', nombreArtista);
        formData.append('nombre_album', nombreAlbum);
        formData.append('url_imagen', urlImagen);
        formData.append('duracion', duracion);
        fromData.append('url_cancion', urlCancion)

        // Obtener el token CSRF de la cookie
        const csrftoken = getCookie('csrftoken');

        // Enviar la solicitud AJAX con fetch
        fetch('create', {
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
            window.location.href = `/musicterritory/playlists/${playlistId}`;
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