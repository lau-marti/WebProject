const SpotifyWebApi = require('spotify-web-api-node');
const readline = require('readline');

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
  await obtenerToken();

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.question('Introduce el nombre de la canción: ', async (nombreCancion) => {
    rl.close();

    try {
      const response = await spotifyApi.searchTracks('track:' + nombreCancion, { limit: 5 });

      if (response.body.tracks.items.length > 0) {
        console.log("Se encontraron las siguientes canciones:");

        for (let i = 0; i < response.body.tracks.items.length; i++) {
          const cancion = response.body.tracks.items[i];
          console.log(`Canción ${i + 1}:`);
          console.log("Nombre:", cancion.name);
          console.log("Artista(s):", cancion.artists.map(artist => artist.name).join(", "));
          console.log("Álbum:", cancion.album.name);
          console.log("URL del álbum:", cancion.album.external_urls.spotify);
          console.log("URL de la imagen del álbum:", cancion.album.images[0].url);

          // Obtener los géneros de los artistas asociados
          const artistasIds = cancion.artists.map(artist => artist.id);
          const artistasInfo = await Promise.all(artistasIds.map(artistId => spotifyApi.getArtist(artistId)));

          console.log("Género(s):", artistasInfo.map(artistInfo => artistInfo.body.genres.join(", ")).join(", "));
          console.log("--------------------");
        }
      } else {
        console.log("No se encontraron canciones con ese nombre.");
      }
    } catch (error) {
      console.error("Error al buscar la canción:", error);
    }
  });
}

// Ejemplo de uso
buscarCancion();
