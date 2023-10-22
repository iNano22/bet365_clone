        // Function to set the data-id attribute based on the matchId query parameter
        function setMatchIdFromQueryParam() {
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const matchId = urlParams.get('matchId');

            // Find the widget container
            const widgetContainer = document.getElementById('wg-api-football-game');

            // Set the data-id attribute if matchId is present
            if (matchId && widgetContainer) {
                widgetContainer.setAttribute('data-id', matchId);
            }
        }

        // Call the function when the page loads
        window.addEventListener('DOMContentLoaded', function () {
            setMatchIdFromQueryParam();
        });