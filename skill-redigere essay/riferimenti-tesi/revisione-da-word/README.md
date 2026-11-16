# `tools/revisione/` — la revisione del documento finito

Questi strumenti non fanno parte della pipeline di stesura. Quella andava dall'Excel al
Word; questa parte dal Word e non torna indietro.

La differenza non è organizzativa, è di regola. La pipeline aveva una regola sovrana:
nessuna affermazione fuori dalla colonna `Descrizione` dell'iTOC. Qui **quella regola non
vale più**: l'autore ha riscritto, fuso e aggiunto lavorando dentro Word, e ne aveva il
diritto. L'iTOC resta come materiale di verifica — le `Descrizione`, le fonti ammesse e
vietate, le coppie di `Estratti` — non come metro di conformità.

Tutto è **read-only sul documento**. Nessuno strumento qui dentro scrive in `out/`.

## L'ordine, e perché è quello

```
estrai_docx.py      il .docx → uno snapshot congelato + doc.json + doc.md
estrai_prof.py      il commento del relatore → professore.md, numerato per punti
mappa_nodi.py       sezioni del documento ↔ nodi dell'iTOC, con allineamento ordinato
  ↓
lint_citazioni_doc.py   testo ↔ bibliografia ↔ tesi.bib
lint_plagio_doc.py      n-grammi e parafrasi contro i 68 testi estratti
lint_lessico_doc.py     glossario, varianti, regole di stesura + concordanza.md
lint_numeri_doc.py      cifre, date e nomi propri contro la whitelist dell'Excel
lint_struttura_doc.py   numerazione stampata, rimandi interni, titoli, tabelle
  ↓
            [ gli agenti: doc-*-auditor, in doppia istanza ]
  ↓
valida_findings.py  i rilievi degli agenti sono ancorati a testo che esiste?
  ↓
rimedio (agente) → verifica_rimedi.py → componi_referto.py
  ↓
stato.py            cosa e' stato applicato, cosa rifiutato, quali capitoli sono cambiati
```

`esegui_lint.py` esegue da solo tutta la parte deterministica, autotest compresi.
`comune.py` tiene le decisioni che devono essere uguali per tutti: cos'è prosa, cosa sono
i ringraziamenti, cos'è appendice, come si spezzano le frasi.

## Le tre idee che reggono il tutto

**Lo snapshot.** Il `.docx` è un file che l'autore tiene aperto in Word mentre la revisione
gira. Se ogni strumento lo rileggesse, lavorerebbero su testi diversi e i rimedi non si
applicherebbero. Si legge una volta, si congela, e da lì in poi la verità è il JSON.
`esegui_lint.py` si rifiuta di rigenerare lo snapshot se ci sono referti di agenti più
recenti: cambierebbe le ancore sotto i loro rilievi.

**L'ancora.** Ogni paragrafo ha un identificatore `P123`, stabile dentro uno snapshot. Un
rilievo cita sempre l'ancora *e* il testo esatto: l'ancora per ritrovare il punto adesso,
il testo perché al giro dopo le ancore cambiano e il testo no.

**L'autotest.** Ogni strumento ha `--autotest`, e non è cerimonia. Un linter che si rompe
non produce rilievi sbagliati: produce **zero** rilievi, che a occhio somiglia a un
documento pulito. Dove è stato possibile, l'autotest è ancorato a una verità nota invece
che a un caso costruito:

- `lint_citazioni_doc.py` deve trovare esattamente le quattro voci di bibliografia mai
  citate — le stesse quattro che l'autore si è annotato in un commento dentro il Word. Ha
  cominciato trovandone quattordici: dieci erano cognomi con la particella (`del Sol`,
  `den Hertog`, `von Nordenflycht`) che la regex leggeva a metà;
- `lint_struttura_doc.py` deve ricostruire la numerazione stampata e ritrovare «0» sul
  primo capitolo e «5» sul capitolo ELFO, come nel PDF impaginato;
- `verifica_rimedi.py` deve bocciare un rimedio la cui fonte non dice quello che gli si fa
  dire, e lasciar passare quello la cui prova esiste davvero nel testo estratto.

## Cosa hanno già trovato, la prima volta che hanno girato

Non è un elenco di vittorie: serve a sapere cosa aspettarsi e cosa no.

- una sequenza di dieci parole identica a Reed & DeFillippi (1990), senza virgolette;
- un paragrafo in italiano dentro il Cap. 5 (l'autore lo sapeva: c'è il suo commento);
- «section 5.1.2» che dopo la fusione delle sezioni del metodo arriva a una sezione diversa
  da quella a cui puntava;
- la nota metodologica Orbis + Apollo con nove valori (2.495 imprese, i codici NACE, la
  soglia di fatturato, la data) che non hanno origine in nessun materiale del progetto:
  sono stati aggiunti in Word dopo il rilievo del relatore, e vanno documentati;
- «CONCLUSION» scritto con lo stile del corpo del testo: non entra nell'indice;
- 642 parole di `Descrizione` sul metodo compresse in due sezioni, proprio dove il relatore
  dice che il metodo è debole.

## Le trappole, quelle vere

- **`/usr/bin/python3`**, non il `python3` di default (miniconda, senza `openpyxl` né
  `python-docx`).
- **`out/` non esiste nei worktree**: è ignorato da git. La revisione gira dal checkout
  principale.
- **Un file `~$LF….docx` significa che Word ha il documento aperto**: si legge l'ultimo
  salvataggio, e lo strumento lo dice. Non cancellarlo mai.
- **Le ancore cambiano fra due snapshot.** Un rimedio del giro scorso si ritrova col
  `trova`, non con `P123`.
- **Il corpus del plagio pesa 4,4 MB**: la prima passata impiega una ventina di secondi.
  È l'unico strumento lento.
