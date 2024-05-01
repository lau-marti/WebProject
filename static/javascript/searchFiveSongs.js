// Inicializar el cliente de SpotifyWebApi
const spotifyApi = new SpotifyWebApi({
  clientId: '7f44fa05891c4b0388022a3317aea4cb',
  clientSecret: 'd9e691dd766a45509a5f4f9b8ce026c6'
});

// Función para obtener un token de acceso utilizando Client Credentials Flow
function obtenerToken() {
  return fetch('https://accounts.spotify.com/api/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic ' + btoa('7f44fa05891c4b0388022a3317aea4cb:d9e691dd766a45509a5f4f9b8ce026c6')
    },
    body: 'grant_type=client_credentials'
  })
  .then(response => response.json())
  .then(data => {
    spotifyApi.setAccessToken(data.access_token);
  })
  .catch(error => {
    console.error("Error al obtener el token de acceso:", error);
  });
}

// Función para buscar información de una canción
function buscarCancion() {
  const nombreCancion = document.getElementById('searchInput').value;
  obtenerToken()
    .then(() => {
      spotifyApi.searchTracks('track:' + nombreCancion, { limit: 10 })
        .then(response => {
          if (response.body.tracks.items.length > 0) {
            const searchResults = document.getElementById('searchResults');
            searchResults.innerHTML = ''; // Limpiar resultados anteriores

            console.log("Se encontraron las siguientes canciones:");
            for (let i = 0; i < response.body.tracks.items.length; i++) {
              const cancion = response.body.tracks.items[i];
              const artistasIds = cancion.artists.map(artist => artist.id);
              Promise.all(artistasIds.map(artistId => spotifyApi.getArtist(artistId)))
                .then(artistasInfo => {
                  const resultDiv = document.createElement('div');
                  resultDiv.innerHTML = `
                    <p>Canción ${i + 1}:</p>
                    <p> Nombre: ${cancion.name}</p>
                    <p> Artista(s): ${cancion.artists.map(artist => artist.name).join(", ")}</p>
                    <p> Álbum: ${cancion.album.name}</p>
                    <p> URL del álbum: <a href="${cancion.album.external_urls.spotify}" target="_blank">${cancion.album.external_urls.spotify}</a></p>
                    <p> URL de la imagen del álbum: <img src="${cancion.album.images[0].url}" alt="Imagen del álbum"></p>
                    <p> Género(s): ${artistasInfo.map(artistInfo => artistInfo.body.genres.join(", ")).join(", ")}</p>
                    <hr>
                  `;
                  searchResults.appendChild(resultDiv);
                });
            }
          } else {
            console.log("No se encontraron canciones con ese nombre.");
          }
        })
        .catch(error => {
          console.error("Error al buscar la canción:", error);
        });
    });
}
