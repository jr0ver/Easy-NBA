document.addEventListener('DOMContentLoaded', () => {
    const deleteButton = document.getElementById('delete-btn');
    console.log("test");
    console.log(deleteButton);

    if (deleteButton) {
        deleteButton.addEventListener('click', (event) => {
            const playerId = event.target.getAttribute('data-player-id');
            deletePlayer(playerId);
        });
    }
});

function deletePlayer(playerId) {
    fetch('/delete_player', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ player_id: playerId })
    })
    .then(response => {
        // check if we were redirected
        if (response.ok) {
            console.log('Deletion successful, reloading page');
            alert('Player updated successfully! Refreshing page');
            // reload the page after successful deletion
            window.location.reload();
        } else {
            console.log('Something went wrong or no redirect');
            alert('Oops! There was an error updating the player. Try refreshing the page');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error with the deletion process.');
    });
}
