# Italian Weather App

Piccolo esercizio front-end per esercitarsi con **fetch API**, **Promise** e gestione asincrona in JavaScript vanilla, usando le API di [OpenWeatherMap](https://openweathermap.org/api) per mostrare il meteo di alcune città italiane.

## Funzionalità

- **Città singola**: seleziona una città da un menu a tendina e visualizza temperatura, descrizione e icona meteo
- **Tutte le città insieme** (`Promise.all`): recupera i dati meteo di 7 città italiane (Milano, Roma, Bologna, Palermo, Napoli, Torino, Firenze) in parallelo, mostrandole tutte insieme al termine di tutte le richieste
- **Tutte le città una alla volta**: recupera e mostra i dati delle stesse 7 città in sequenza, con un breve ritardo tra una card e l'altra, per visualizzare l'effetto delle chiamate asincrone eseguite in ordine

## Obiettivo

L'esercizio confronta due strategie diverse per gestire più richieste asincrone:
- `Promise.all` per l'esecuzione **parallela**
- `setTimeout` + `forEach` per l'esecuzione **sequenziale/scaglionata** 

## Tecnologie

- HTML5 / CSS3
- JavaScript (vanilla, `fetch`, `Promise`)
- [Bootstrap 5](https://getbootstrap.com/) (CDN, per lo stile)
- [OpenWeatherMap API](https://openweathermap.org/api)


## Prima di eseguirlo

Il file `index.js` richiede una API key valida di OpenWeatherMap:

```js
const apiKey = "LA_TUA_API_KEY";
```

Registrati gratuitamente su [openweathermap.org](https://home.openweathermap.org/users/sign_up), genera una chiave dalla tua dashboard e sostituiscila nel codice prima di avviare il progetto. Le chiavi gratuite possono richiedere alcuni minuti/ore per attivarsi dopo la registrazione.


## Come avviarlo

Non è richiesto alcun processo di build. Due opzioni:

**1. Apertura diretta**
Apri semplicemente `index.html` nel browser.

**2. Con un server locale**

Con VS Code, installa l'estensione **Live Server** e avvia il progetto con tasto destro su `index.html` → *Open with Live Server*.

Oppure, da terminale:

```bash
cd weather-exercise

# con Python
python3 -m http.server 8000

# oppure con Node.js
npx serve .
```

Poi apri `http://localhost:8000` (o la porta indicata) nel browser.
