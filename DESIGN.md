# Roseto & Dintorni — contratto di design

## Direzione

Un giornale di servizio locale per scegliere cosa fare sulla costa, non una landing promozionale. La pagina deve sembrare curata da una piccola redazione: titoli netti, date subito leggibili, gerarchia editoriale, spazio bianco e dettagli utili prima dell'effetto.

**Tesi:** la costa adriatica si riconosce nel ritmo tra luogo, ora e appuntamento; non servono cartoline, onde decorative o fotografie generiche.

## Sistema visivo

- **Palette:** carta calda `#f4f0e8`, inchiostro `#17242a`, blu petrolio `#0d3b45`, rosso corallo `#d95d45`, giallo sole `#e8b34a`, grigio sale `#6a7778`. Il fondo chiaro è la modalità principale; il petrolio è riservato a testata, hero editoriale e azioni forti.
- **Tipografia:** `Fraunces` per titoli e numeri, `DM Sans` per interfaccia e testi. Caratteri con fallback di sistema; nessuna icona-font necessaria. I titoli devono avere contrasto di scala, non maiuscole ovunque.
- **Forma:** bordi sottili e angoli misurati (4–18px); niente vetro, blur, ombre flottanti o gradienti decorativi. Le immagini ufficiali restano immagini, senza filtri o sostituzioni.
- **Segno adriatico:** righe, coordinate, etichette di redazione, accenti corallo/sole e composizione asimmetrica. Mai cliché marini, foto stock o placeholder figurativi.

## Composizione

1. Testata compatta con nome, stato di aggiornamento e navigazione testuale.
2. Apertura editoriale a due colonne su desktop, con titolo e breve promessa di servizio; su mobile una colonna.
3. Strumenti di ricerca/filtro sempre raggiungibili, con input nativo e chip scrollabili.
4. Un solo appuntamento in evidenza, trattato come apertura giornalistica.
5. Elenco eventi raggruppato per data e città. Le card sono righe editoriali / blocchi irregolari, non una griglia seriale di tile SaaS.
6. Sponsor chiaramente separato e richiudibile, navetta come servizio pratico, sagre e archivio come viste coerenti.
7. Footer con fonte/aggiornamento. Barra mobile essenziale; navigazione desktop leggibile.

## Regole editoriali

- Mostrare prima: giorno, titolo, città/luogo, orario e costo. Descrizioni brevi e leggibili.
- Non riscrivere, inventare o normalizzare il contenuto dei dataset: `data/events.json` e `data/sagre.json` sono sorgenti immutabili.
- `image` vuoto significa nessuna immagine: rendere il blocco tipografico con colore piatto e iniziali, mai generare un'immagine, usare stock, Unsplash, Picsum o una foto del luogo.
- Ogni link esterno conserva la fonte e apre in nuova scheda con `noopener`.
- Niente slogan vuoti: il testo UI deve spiegare cosa si può fare.

## Accessibilità e comportamento

- Landmark semantici, una sola gerarchia H1 per vista, label associate, `aria-live` per conteggi/errori, focus visibile e contrasto WCAG AA.
- Target interattivi almeno 44px; nessuna informazione affidata solo al colore.
- `prefers-reduced-motion: reduce` disattiva reveal, hover trasformativi, scroll animato e animazioni decorative.
- La ricerca, filtri città/provincia/periodo, archivio, sagre, navetta, sponsor, contatore, lightbox, PWA, service worker, SEO, structured data, link, aggiornamento e deploy restano funzionanti.

## Vincoli tecnici

- Una pagina statica, CSS e JavaScript vanilla; niente nuove dipendenze runtime. I font remoti esistenti possono restare solo se migliorano davvero il risultato e con fallback.
- Modifiche ammesse a `index.html`, `DESIGN.md` e asset strettamente necessari. Non modificare semantica o contenuto dei dataset.
- Prima del rilascio: validazione dati, sintassi JavaScript, integrità PWA/SEO/link, controllo overflow/testi lunghi, tastiera/focus/contrasto/landmark/target touch/reduced motion, console e interazioni, `git diff --check` e tutte le verifiche presenti nel repository.
