<!--
SCALETTA — il contratto del testo.

La scrive l'autore, da solo o passo per passo con Claude (skill essay-scaletta),
DOPO aver letto intermedi/matrice.md, intermedi/punti.md e le sintesi per domanda.
La prosa di ogni sezione potrà contenere SOLO ciò che sta nel suo testo libero
(«contenuto») e nei «punti» che elenca. Tutto il resto il writer lo dichiara come
buco, non lo inventa.

Sintassi (la legge tools/scaletta/leggi_scaletta.py):

  # Titolo dell'essay
  ## <id> <titolo>            livello 1 (id = primo token: 1, 2, intro, ...)
  ### <id> <titolo>           livello 2
  #### <id> <titolo>          livello 3
  parole: 300                 lunghezza obiettivo della sezione
  ruolo: deve dimostrare che  cosa la sezione deve ottenere nell'argomento
  punti: fonte#1, fonte#4     punti validati da usare (id da intermedi/punti.md)
  aggancio: verso 2 ...       transizione richiesta verso la sezione dopo
  trappole: non dire che ...  rischi da evitare (li controlla l'auditor)
  escludi: sì                 sezione presente in scaletta ma non da scrivere
  tutto il resto              = contenuto, il tuo materiale: idee, argomenti, esempi

Quanto scrivere nel contenuto: più è argomentato, più il testo sarà tuo.
Se una sezione ha poco materiale rispetto alle parole, uscirà corta: il writer
non riempie (non esiste un pavimento di parole). leggi_scaletta.py te lo segnala.

Cancella l'esempio qui sotto e scrivi la tua.
-->

# Titolo dell'essay

## 1 Introduction
parole: 300
ruolo: presentare il problema e la tesi dell'essay
aggancio: verso 2, dal problema al meccanismo che lo spiega
Il problema è ... La tesi sostenuta è che ...

## 2 Primo argomento
parole: 800
ruolo: deve dimostrare che ...
punti: esempio2020#1, esempio2020#3
trappole: non attribuire alla fonte l'estensione al caso
Il punto di partenza è ... Applicato al caso, questo significa ...

### 2.1 Sottosezione
parole: 400
ruolo: ...
punti: altrafonte2019#2
...

## 3 Conclusion
parole: 300
ruolo: chiudere riprendendo la tesi, senza materiale nuovo
...
