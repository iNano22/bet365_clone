// Function to handle match rows
function handleMatchRows() {
    const matchRows = document.querySelectorAll('.football-games-select');

    matchRows.forEach(function (row) {
        const matchId = row.id.replace('football-game-', '');
        const status = row.getAttribute('data-status');

        // Remove the status check to make all rows clickable
        if (!row.hasAttribute('data-clickable')) {
            // Mark the row as clickable using a custom attribute
            row.setAttribute('data-clickable', 'true');

            row.addEventListener('click', function () {
                // Open game.html in a new tab with the match ID in the query parameter
                window.open(`game.html?matchId=${matchId}`, '_blank');
            });

            // Add hover effect using JavaScript
            row.addEventListener('mouseover', function () {
                row.style.backgroundColor = '#f0f0f0'; // Change the background color on hover
            });

            row.addEventListener('mouseout', function () {
                row.style.backgroundColor = ''; // Reset the background color on mouseout
            });
        }
    });
}

// Function to observe changes in the widget container
function observeWidgetContainer() {
    const widgetContainer = document.querySelector('#wg-api-football-games');
    const observer = new MutationObserver(function () {
        handleMatchRows();
    });

    observer.observe(widgetContainer, { childList: true, subtree: true }); // Observe the subtree
}

// Wait for the widget to load
window.addEventListener('load', function () {
    // Check every 500 milliseconds if the widget content has loaded
    const interval = setInterval(function () {
        const toolbar = document.querySelector('.wg_toolbar');

        if (toolbar) {
            clearInterval(interval); // Stop checking
            handleMatchRows();
            observeWidgetContainer();
        }
    }, 500);
});
