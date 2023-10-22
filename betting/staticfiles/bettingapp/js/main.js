document.addEventListener('click', function (event) {
    if (!event.target.matches('._link')) return
    event.preventDefault()

    let league_id = event.target.getAttribute('data-league')
    let season = event.target.getAttribute('data-season')

    let games = document.getElementById('wg-api-football-games')
    games.innerHTML = ''
    games.setAttribute('data-league', league_id);
    games.setAttribute('data-season', season);

    // Trigger a "DOMContentLoaded" event
    window.document.dispatchEvent(new Event("DOMContentLoaded", {
        bubbles: true,
        cancelable: true
    }));
})


