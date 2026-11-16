# Redigere essay — come si usa

Cartella modello per scrivere un lavoro accademico breve con Claude, dalle fonti al Word.
È la pipeline della tesi, ridotta. Il perché di tutto sta in `PROCESSO.md`; le regole per Claude
in `CLAUDE.md`.

## Per ogni nuovo lavoro

1. **Copia questa cartella** dove serve e rinominala (es. `essay corso X`). Non lavorare
   nell'originale: resta il modello pulito. `riferimenti-tesi/` puoi anche cancellarla dalla copia.
2. Apri la copia in Claude Code e scrivi **`/essay-avvio`**. Ti chiede cosa manca.
3. Riempi (o fatti aiutare a riempire):
   - `progetto.json` — titolo, lingua, parole, nomi fissi, email per le API;
   - `input/brief.md` — consegna, tesi, **domande per le fonti**, idee tue;
   - `input/fonti.csv` — una riga per fonte, basta `id,autori,anno` (id tipo `akerlof1970`);
   - `input/template.docx` — **il template Word: senza, il Word finale non si genera**.
     Puoi metterci `{{TITOLO}}`, `{{AUTORE}}` e un paragrafo `{{CORPO}}` dove va il testo.
4. Poi, in ordine:

| Comando | Cosa fa | Tu cosa fai |
|---|---|---|
| `/essay-fonti` | cerca e scarica le fonti, estrae i testi, fa il `.bib` | scarichi i paywall a mano |
| `/essay-estrai` | un lettore per fonte estrae le risposte alle tue domande, uno script verifica ogni citazione | niente, o decidi le divergenze |
| `/essay-intermedi` | schede, matrice domanda × fonte, sintesi per domanda | **leggi**: è da qui che imposti l'argomento |
| `/essay-scaletta` | ti aiuta a scrivere la scaletta passo per passo e la controlla | **scrivi la scaletta**: è il contratto del testo |
| `/essay-glossario` | (facoltativo) termini vincolanti | approvi |
| `/essay-scrivi` | scrive una sezione alla volta, controlla ognuna | **approvi la prima** (pilota) |
| `/essay-controlla` | auditor, correzioni, escalation | **decidi** i buchi e le escalation |
| `/essay-word` | assembla il Word dal tuo template | rileggi |

`/essay-stato` in qualunque momento ti dice dove sei e cosa viene dopo.

## Due cose da sapere

- **Il testo non conterrà niente che non sia nella tua scaletta o nelle fonti validate.** Se
  manca qualcosa, Claude mette `[[GAP: motivo]]` e te lo chiede, non lo inventa. Più metti nella
  scaletta, più il testo è tuo.
- **Se hai già i PDF**, mettili in `fonti/pdf/<id>.pdf` e nel CSV scrivi `gia_presente` nella
  colonna `stato`. Per pagine web o appunti, metti il testo in `fonti/testi/<id>.txt`.

## Requisiti

`python3` con `requests`, `openpyxl`, `python-docx` (quello di miniconda li ha), e `pdftotext`
(`brew install poppler`). Per il secondo lettore, NotebookLM collegato.
