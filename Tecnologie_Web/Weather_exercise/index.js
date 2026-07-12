/* const apiKey = "36810e00a822f28c19aa8db6e1ac4694"; //metti qui la tua chiave
const citySelect = document.getElementById("city-select");
const weatherCards = document.getElementById("weather-cards"); //div to fill with weather cards
const form = document.getElementById("city-form"); //form to get the city
// const cities = ["Milano", "Roma", "Bologna", "Palermo", "Napoli", "Torino", "Firenze"];
//for the home exercise using Promise.all

function clearWeatherCards() {
  weatherCards.innerHTML = '';
  //removes the weather cards from the div
}

function getWeather(selectedCity, apiKey) {
  clearWeatherCards()
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${selectedCity}&lang=it&units=metric&appid=${apiKey}`;
  console.log(url)




  //completa la funzione
}

//oppure: 
// async function getWeather(selectedCity, apiKey) {
//   const url = `https://api.openweathermap.org/data/2.5/weather?q=${selectedCity}&lang=it&units=metric&appid=${apiKey}`;
//   riempi se vuoi usare invece async await
//}

form.addEventListener("submit", event => {
  event.preventDefault(); // prevents form from refreshing page
  const selectedCity = document.getElementById("city-select").value;
  getWeather(selectedCity, apiKey);
}); */


const apiKey = "36810e00a822f28c19aa8db6e1ac4694"
const citySelect = document.getElementById("city-select");
const weatherCards = document.getElementById("weather-cards"); //div to fill with weather cards
const form = document.getElementById("city-form"); //form to get the city
const cities = ["Milano", "Roma", "Bologna", "Palermo", "Napoli", "Torino", "Firenze"];
const getAllTogetherButton = document.getElementById("all-cities-sync");
const getOneByOneButton = document.getElementById("all-cities");

function clearWeatherCards() {
  weatherCards.innerHTML = '';
}

// --------------- CITTA' SINGOLA ---------------

function getWeather(selectedCity) {
  clearWeatherCards();
  const url = getUrl(selectedCity);
  fetch(url)
      .then(response => response.json())
      .then(data => {
        //console.log(data);
        weatherCards.innerHTML = displayWeather(data);
      })
      .catch(error => console.log(error));
}

// --------------- PROMISE ALL ---------------

function getAllTogether(){
  clearWeatherCards();
  setTimeout(() => {
    const promises = cities.map(city => {
      const url = getUrl(city);
      return fetch(url)
          .then((response) => response.json())
          .then((data) => {
            const cardHTML = displayWeather(data);
            return cardHTML;
          })
          .catch((err) => console.log(err));
    })
    Promise.all(promises)
        .then(cards => {
          weatherCards.innerHTML = cards.join('');
        }).catch(err => console.log(err));
  }, 1000);
}

// --------------- ONE BY ONE ---------------

function getOneByOne() {
  clearWeatherCards();
  cities.forEach((city, index) => {
    setTimeout(() => {
      const url = getUrl(city)
      fetch(url)
          .then(response => response.json())
          .then(data => {
            //console.log(data);
            weatherCards.innerHTML += displayWeather(data);
          })
          .catch(error => console.log(error));
    }, index*1000)
  });
}

// --------------- LISTENERS ---------------

form.addEventListener("submit", event => {
  event.preventDefault(); // prevents form from refreshing page
  const selectedCity = document.getElementById("city-select").value;
  getWeather(selectedCity);
});

getAllTogetherButton.addEventListener("click", event => {
  event.preventDefault(); // prevents form from refreshing page
  getAllTogether();
});

getOneByOneButton.addEventListener("click", event => {
  event.preventDefault(); // prevents form from refreshing page
  getOneByOne();
});

// --------------- HTML CARD GENERATOR ---------------

function displayWeather(data){
  const city = data.name;
  const temp = data.main.temp;
  const descr = data.weather[0].description;
  const icon = 'http://openweathermap.org/img/wn/' + data.weather[0].icon + '.png';
  return `<div class="card">
            <div class="card-body">
              <h5 class="card-title">${city}</h5>
              <img class="card-img-top" src=${icon} alt="Title">
              <p class="card-text">${temp}</p>
              <p class="card-text">${descr}</p>
            </div>
          </div>`;
}

// --------------- URL ---------------

function getUrl(city){
  return `https://api.openweathermap.org/data/2.5/weather?q=${city}&lang=it&units=metric&appid=${apiKey}`;
}




