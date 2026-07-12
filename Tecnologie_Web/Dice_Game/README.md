# Dicee Challenge

Esercizio front-end che simula il lancio di due dadi per una sfida a due giocatori, usando JavaScript vanilla per generare numeri casuali e manipolare il DOM.

## Come funziona

Ad ogni **refresh della pagina**:
1. Vengono generati due numeri casuali (1-6), uno per giocatore
2. Le immagini dei dadi vengono aggiornate di conseguenza
3. Il titolo della pagina mostra il risultato: vince chi ha il numero più alto, oppure viene dichiarato un pareggio

Non essendoci un pulsante di lancio, il "tira i dadi" avviene semplicemente ricaricando la pagina (da cui il titolo "Refresh Me!").

## Obiettivo

Esercizio introduttivo su:
- generazione di numeri casuali con `Math.random()`
- selezione e manipolazione di elementi DOM (`querySelector`, `querySelectorAll`, `setAttribute`)
- logica condizionale semplice per confrontare due valori

## Tecnologie

- HTML5 / CSS3 (font Google: *Lobster*, *Indie Flower*)
- JavaScript vanilla (nessuna libreria o dipendenza esterna)


## Come avviarlo

Non è richiesto alcun processo di build o installazione di dipendenze.

**1. Apertura diretta**
Apri semplicemente `dicee.html` nel browser.

**2. Con un server locale (opzionale)**

```bash
cd "Dicee Challenge"

# con Python
python3 -m http.server 8000

# oppure con Node.js
npx serve .
```

Poi apri `http://localhost:8000` nel browser.
