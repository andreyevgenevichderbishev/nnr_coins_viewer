let currentPage = 0;
const coinsPerPage = 5;
let allCoins = [];

// Функция для загрузки монет
async function loadCoins() {
    const response = await fetch('/coins');
    const data = await response.json();
    allCoins = data;
    displayCoins();
}

// Функция для отображения монет
function displayCoins() {
    const coinList = document.getElementById('coin-list');
    const loading = document.getElementById('loading');

    // Очистка списка перед добавлением новых монет
    coinList.innerHTML = '';

    // Выбор текущей порции монет
    const start = currentPage * coinsPerPage;
    const end = start + coinsPerPage;
    const coinsToShow = allCoins.slice(start, end);

    // Добавление монет в список
    coinsToShow.forEach(coin => {
        const coinItem = document.createElement('div');
        coinItem.className = 'coin-item';
        coinItem.innerHTML = `
            <h2>${coin.number}</h2>
            <p>Year: ${coin.year}</p>
            <p>Country: ${coin.value}</p>
            <div class="images">
                <img src="D:\Python\coin_pages\${coin.avers}.jpg" alt="Avers">
                <img src="D:\Python\coin_pages\${coin.revers}.jpg" alt="Revers">
            </div>
        `;
        coinList.appendChild(coinItem);
    });

    // Показать/скрыть индикатор загрузки
    if (end >= allCoins.length) {
        loading.style.display = 'none';
    } else {
        loading.style.display = 'block';
    }
}

// Функция для обработки скроллинга
window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    if (scrollTop + clientHeight >= scrollHeight - 5) {
        currentPage++;
        displayCoins();
    }
});

// Загрузка монет при загрузке страницы
window.onload = loadCoins;