# ToDo List 

Applicazione web full-stack per la gestione di una lista di attività, con autenticazione utenti, supporto Markdown per il contenuto e ricerca live.

## Funzionalità

- **Autenticazione utenti** (registrazione, login, logout) con [Passport.js](https://www.passportjs.org/) e password hashate con `bcrypt`
- **Gestione ToDo personali**: ogni utente vede e crea solo le proprie attività
- **Editor con supporto Markdown**: il contenuto dei ToDo viene scritto in Markdown e convertito in HTML lato server
- **Tag**: ogni ToDo può avere più tag, aggiungibili dinamicamente in fase di creazione
- **Ricerca live**: barra di ricerca in-page che interroga titolo e tag dei ToDo mentre si digita
- **Completamento ToDo**: possibilità di marcare/eliminare un'attività come completata
- **Flash messages** per feedback su login falliti e altre azioni


## Requisiti

- Node.js (≥ 16)
- Un cluster MongoDB (locale o [MongoDB Atlas](https://www.mongodb.com/atlas))

## Configurazione — variabili d'ambiente

Il progetto richiede due variabili d'ambiente, da inserire in un file `.env` nella root (non committare mai questo file):

```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
SESSION_SECRET=una-stringa-lunga-e-casuale-generata-da-te
```


## Come avviarlo

```bash
git clone <url-del-repository>
cd todo-app

npm install

cp .env
# compila .env con la tua MONGODB_URI e SESSION_SECRET

npm start
```

L'app sarà disponibile su `http://localhost:3000`.

Per lo sviluppo, con auto-reload sui cambi di codice (usando `nodemon`, già tra le dipendenze):

```bash
npx nodemon index.js
```
