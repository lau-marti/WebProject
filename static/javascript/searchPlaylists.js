function buscarPlaylist(event) {

    event.preventDefault();

    var searchValue = document.getElementById('searchPlaylist').value;

    $.ajax({
        url: '/musicterritory/search_playlists/',
        method: 'GET',
        data: {
            'searchValue': searchValue
        },
        success: function(response) {
            var resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = ''; // Limpiar los resultados anteriores

            if (response.playlists.length === 0) {

                resultsDiv.textContent = 'No existen playlists con ese nombre. Porfavor intentalo de nuevo';
            } else {
                response.playlists.forEach(function(playlist) {

                    var resultButton = document.createElement('button');
                    resultButton.textContent = playlist.name + ' - ' + playlist.user;
                    resultButton.className = 'playlistButton'
                    resultButton.onclick = function() {
                        window.location.href = '/musicterritory/playlists/' + playlist.id;
                    };

                    resultsDiv.appendChild(resultButton);

                    // Per a fer un salt de linia, que els botons apareguin en linies diferents
                    resultsDiv.appendChild(document.createElement('br'));
                });
            }
        },
        error: function(xhr, status, error) {
            console.error("Error al buscar las playlists:", error);
        }
    });
}
