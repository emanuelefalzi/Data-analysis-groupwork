---
name: tesi-frontmatter
description: Invoca l'agente front-back-matter per scrivere abstract e introduzione. Gira solo dopo l'ultimo capitolo (Cap. 6) e dopo /tesi-audit --whole, mai prima. Bloccata finché GATE 1 non ha detto dove vivono introduzione, abstract e reference list. L'abstract non entra mai in out/tesi.docx.
---

# /tesi-frontmatter

Invoca l'agente `front-back-matter` (Sonnet, `.claude/agents/front-back-matter.md`).
Non scrive prosa essa stessa: prepara l'input dell'agente, lo invoca, e verifica
l'output. I due testi che nessun nodo dell'Excel contiene — abstract e
introduzione — esistono solo dopo che i capitoli esistono: prima non c'è niente
da riassumere.

## Precondizioni

1. **Tutti i capitoli 0-6 hanno `DRAFT` completo** in `nodes/*.md` (il Cap. 7 è
   sospeso e resta fuori, non è una precondizione mancata). Verificalo da
   `build/nodes.json` (`stato: "scritto"` su ogni nodo in perimetro non
   `⚠ RICHIESTA AUTORE`) o da `/tesi-status`. Se manca anche un solo nodo, fermati:
   questa skill non gira "nel frattempo".
2. **`/tesi-audit --whole` è già girato**, con il suo esito registrato (report
   `reports/audit-whole.md` o equivalente). Non basta che i singoli
   `/tesi-audit <capitolo>` siano puliti: `--whole` cerca la ridondanza fra
   capitoli, che per capitolo non si vede, ed è esplicitamente il gate prima di
   questa skill (§5, §10 del prompt orchestratore).
3. **GATE 1, domanda 3, ha risposta**: dove vivono abstract, introduzione e
   reference list, registrata in `decisions/DECISIONS.md`. Senza risposta questa
   skill **non si rifiuta di girare** — l'agente produce comunque il contenuto,
   con la nota di posizione non decisa (vedi sotto) — ma **`/tesi-assemble` sì**:
   non inserire mai tu quel contenuto nel documento per aggirare il blocco.
4. Nessun lock file (`~$*`) su `def titolo C_EN.docx`: lo apri tu in sola
   lettura al passo 1, non l'agente.

## Passi

### 0. Verifica le precondizioni

Come sopra. Se una manca, fermati e dillo — non procedere "per intanto solo
sull'abstract" o simili scorciatoie.

### 1. Estrai il materiale dell'abstract già scritto (compito tuo, mai dell'agente)

`front-back-matter` non apre mai `def titolo C_EN.docx`, in nessuna circostanza
(vedi l'agente, § "Cosa ricevi in input" / "Divieti"). L'abstract che l'autore ha
già scritto lì non è per questo perso: **tu**, l'orchestratore, lo leggi in sola
lettura e ne estrai il testo, poi lo consegni all'agente come materiale in
chiaro, non come file da aprire da solo.

Nel documento il testo dell'abstract sta fra il paragrafo con stile `grasso
titoli` e testo `Abstract` e il paragrafo successivo con lo stesso stile
(oggi `Logic`) — verificato sul file reale:

```bash
/usr/bin/python3 - <<'PYEOF'
import docx
BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
d = docx.Document(BASE + "def titolo C_EN.docx")
paras = d.paragraphs
start = next(i for i, p in enumerate(paras)
             if p.style.name == "grasso titoli" and p.text.strip() == "Abstract")
end = next(i for i in range(start + 1, len(paras))
           if paras[i].style.name == "grasso titoli")
testo = "\n\n".join(p.text.strip() for p in paras[start + 1:end] if p.text.strip())
nota = (
    "<!-- Materiale in chiaro estratto da `def titolo C_EN.docx` (paragrafo "
    "'Abstract') dalla skill /tesi-frontmatter. L'agente front-back-matter non "
    "apre mai questo file (vedi l'agente, sezione Divieti): riceve solo questo "
    "materiale gia' estratto. Riferimento di sostanza e di tono sull'abstract "
    "gia' scritto dall'autore, non una fonte che scavalca nodes.json: ogni "
    "frase che l'agente ne riusa deve comunque risultare gia' presente in "
    "build/nodes.json o in un DRAFT esistente — la regola sovrana vale anche "
    "su questo file, non e' un lasciapassare. -->\n\n"
)
out = BASE + "build/abstract-materiale.md"
with open(out, "w", encoding="utf-8") as f:
    f.write(nota + testo + "\n")
print(out, len(testo), "caratteri")
PYEOF
```

Scrive **`build/abstract-materiale.md`**: è il file di consegna del materiale,
non un output della pipeline di stesura — non ha un `## DRAFT`/`## LEDGER`, non
lo tocca `/tesi-assemble`, non sostituisce `build/abstract.md` (quello lo scrive
l'agente al passo 2). Se il paragrafo `Abstract` non si trova con questo
criterio (il documento è cambiato), fermati e segnalalo: non indovinare i
confini del testo a occhio.

### 2. Invoca `front-back-matter`

Costruisci il contesto dell'agente con **esattamente**:

- `build/nodes.json` per intero (struttura, `title`, `source_desc`, e in
  particolare `ruolo` dei nodi capofila `0`…`6`);
- i `## DRAFT` di `nodes/*.md` per i capitoli 0-6;
- `FONTI/pipeline/glossario/glossario.json`, in sola lettura;
- i nodi `0.1`, `0.1.1`-`0.1.4`, solo se e quando hanno `source_desc` non vuoto
  (oggi sono vuoti: l'agente dichiara la research question come `[[GAP: …]]`,
  non la inventa — è già la sua regola, non serve che tu la applichi);
- **`build/abstract-materiale.md`** prodotto al passo 1, esplicitamente marcato
  nel prompt come *riferimento di sostanza e di tono sull'abstract già scritto
  dall'autore, non come fonte che scavalca `nodes.json`*: se una frase del
  materiale non trova riscontro in `source_desc` o in un `DRAFT`, l'agente la
  scarta, non la copia;
- lo stato di GATE 1 domanda 3 letto da `decisions/DECISIONS.md` (risposto o no),
  così l'agente scrive comunque la nota di posizione non decisa quando manca.

Invoca l'agente con lo strumento Agent/Task, profilo `front-back-matter` se
disponibile, altrimenti lo stesso brief come prompt su Sonnet — mai su Opus
(CLAUDE.md, "Modelli").

L'agente produce **due file**, secondo la propria specifica (non altri, non con
altri nomi):

- **`build/abstract.md`** — prosa continua, massimo 4.000 caratteri, con una
  riga finale `<!-- caratteri: N -->`;
- **`build/introduzione.md`** — prosa continua, con in testa il commento
  `<!-- POSIZIONE NON DECISA: ... -->` se GATE 1 domanda 3 non ha ancora
  risposta.

## Formato output (riepilogo di questa skill, dopo il passo 2)

```
FRONTMATTER — 2026-09-08
Materiale abstract estratto: build/abstract-materiale.md (N caratteri, da "def titolo C_EN.docx")
Agente invocato: front-back-matter (Sonnet)
Prodotti: build/abstract.md (N caratteri, entro 4.000: sì/no)
          build/introduzione.md (posizione: decisa / NON DECISA)
Capitoli mancanti nel riassunto: nessuno | elenco
```

## Postcondizioni

- `build/abstract-materiale.md` esiste, contiene solo testo estratto
  verbatim da `def titolo C_EN.docx` più il commento di provenienza — mai
  materiale riscritto o interpretato da te in questo passo.
- `build/abstract.md` esiste, è sotto i 4.000 caratteri, e non è mai stato
  inserito in `out/tesi.docx`.
- `build/introduzione.md` esiste; se GATE 1 domanda 3 non ha risposta, porta la
  nota `POSIZIONE NON DECISA` in testa.
- Nessun file in `nodes/`, `build/nodes.json`, `build/estratti.json` o l'Excel
  risulta modificato: l'agente è read-only su tutto tranne i suoi due output.

## Cosa non fa mai

- Non gira prima che tutti i capitoli 0-6 abbiano `DRAFT` e prima di
  `/tesi-audit --whole`: non esiste una versione "parziale" di questa skill.
- Non lascia che l'agente apra `def titolo C_EN.docx`: lo apre e lo estrae solo
  questa skill, una volta, al passo 1.
- Non tratta `build/abstract-materiale.md` come fonte che scavalca la regola
  sovrana: resta materiale di riferimento, non un `source_desc`.
- Non inserisce l'abstract in `out/tesi.docx`, in nessuna fase: va nel form web
  dell'ateneo, a mano, max 4.000 caratteri.
- Non decide da sola dove vive l'introduzione: se GATE 1 domanda 3 non ha
  risposta, produce comunque `build/introduzione.md` con la posizione dichiarata
  non decisa, e lascia a `/tesi-assemble` il rifiuto di inserirla finché manca.
- Non invoca `/tesi-assemble`: è un gate successivo, non un passo di questa
  skill.
