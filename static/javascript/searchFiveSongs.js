const SpotifyWebApi = require('spotify-web-api-node');

// Configurar credenciales de cliente de Spotify
const client_id = '7f44fa05891c4b0388022a3317aea4cb';
const client_secret = 'd9e691dd766a45509a5f4f9b8ce026c6';

// Inicializar el cliente de SpotifyWebApi
const spotifyApi = new SpotifyWebApi({
  clientId: client_id,
  clientSecret: client_secret
});

// Obtener un token de acceso utilizando Client Credentials Flow
async function obtenerToken() {
  try {
    const data = await spotifyApi.clientCredentialsGrant();
    spotifyApi.setAccessToken(data.body.access_token);
  } catch (error) {
    console.error("Error al obtener el token de acceso:", error);
  }
}

// Función para buscar información de una canción
async function buscarCancion() {

  const nombreCancion = document.getElementById('searchInput').value;
  await obtenerToken();
  try {
    const response = await spotifyApi.searchTracks('track:' + nombreCancion, { limit: 5 });

    if (response.body.tracks.items.length > 0) {
      document.getElementById('searchResults').innerHTML = '';

      for (let i = 0; i < response.body.tracks.items.length; i++) {
        const cancion = response.body.tracks.items[i];
        const resultDiv = document.createElement('div');
        resultDiv.innerHTML = `
          <p>Canción ${i + 1}:</p>
          <p>Nombre: ${cancion.name}</p>
          <p>Artista(s): ${cancion.artists.map(artist => artist.name).join(", ")}</p>
          <p>Álbum: ${cancion.album.name}</p>
          <p>URL del álbum: <a href="${cancion.album.external_urls.spotify}" target="_blank">${cancion.album.external_urls.spotify}</a></p>
          <p>URL de la imagen del álbum: <img src="${cancion.album.images[0].url}" alt="Imagen del álbum"></p>
          <p>Género(s): ${await obtenerGenerosArtistas(cancion.artists)}</p>
          <hr>
        `;
        document.getElementById('searchResults').appendChild(resultDiv);

        // Obtener los géneros de los artistas asociados
        //const artistasIds = cancion.artists.map(artist => artist.id);
        //const artistasInfo = await Promise.all(artistasIds.map(artistId => spotifyApi.getArtist(artistId)));

        //console.log("Género(s):", artistasInfo.map(artistInfo => artistInfo.body.genres.join(", ")).join(", "));
        //console.log("--------------------");
      }
    } else {
      document.getElementById('searchResults').innerHTML = 'No se encontraron canciones con ese nombre.';
    }
  } catch (error) {
    console.error("Error al buscar la canción:", error);
  }
}