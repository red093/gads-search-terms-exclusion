# Google Ads Search Terms Analyzer

Script Python per analizzare i termini di ricerca di un account Google Ads e identificare i peggiori performers basati su CPC alto e basso numero di conversioni.

## Caratteristiche

- 🔍 Analizza i termini di ricerca dell'account Google Ads
- 📊 Identifica i 10 peggiori termini basati su:
  - CPC (Cost Per Click) più alto
  - Numero di conversioni più basso
  - Costo totale speso senza conversioni
- 📈 Calcola un "badness score" per ogni termine
- 💾 Esporta i risultati in formato CSV
- ⚙️ Configurabile per diversi periodi di analisi

## Prerequisiti

- Python 3.7 o superiore
- Account Google Ads con accesso API
- Credenziali API Google Ads configurate

## Installazione

1. Clona il repository:
```bash
git clone <repository-url>
cd gads-search-terms-exclusion
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Configura le credenziali Google Ads API:

Crea un file `google-ads.yaml` nella directory del progetto con le tue credenziali:

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
login_customer_id: YOUR_LOGIN_CUSTOMER_ID
use_proto_plus: True
```

### Come ottenere le credenziali API

1. **Developer Token**: Ottienilo dal tuo account Google Ads Manager
   - Vai su Tools & Settings > API Center
   - Richiedi un developer token

2. **OAuth2 Credentials** (client_id, client_secret, refresh_token):
   - Vai alla [Google Cloud Console](https://console.cloud.google.com/)
   - Crea un nuovo progetto o selezionane uno esistente
   - Abilita la Google Ads API
   - Crea credenziali OAuth 2.0
   - Genera un refresh token usando lo script di autenticazione di Google Ads

Per generare il refresh token:
```bash
python -m google.ads.googleads.oauth2.generate_refresh_token \
    --client_id YOUR_CLIENT_ID \
    --client_secret YOUR_CLIENT_SECRET
```

## Utilizzo

### Comando Base

```bash
python search_terms_analyzer.py --customer-id YOUR_CUSTOMER_ID
```

### Opzioni Avanzate

```bash
python search_terms_analyzer.py \
    --customer-id 1234567890 \
    --days 30 \
    --top 10 \
    --config google-ads.yaml \
    --export risultati.csv
```

### Parametri

- `--customer-id`: **(Obbligatorio)** ID del cliente Google Ads (senza trattini)
- `--days`: Numero di giorni da analizzare (default: 30)
- `--top`: Numero di peggiori termini da visualizzare (default: 10)
- `--config`: Path al file di configurazione (default: google-ads.yaml)
- `--export`: Esporta i risultati in un file CSV (opzionale)

## Esempi

### Analizza gli ultimi 30 giorni (default)
```bash
python search_terms_analyzer.py --customer-id 1234567890
```

### Analizza gli ultimi 7 giorni e mostra i top 20
```bash
python search_terms_analyzer.py --customer-id 1234567890 --days 7 --top 20
```

### Esporta i risultati in CSV
```bash
python search_terms_analyzer.py --customer-id 1234567890 --export report.csv
```

## Output

Lo script produce un report formattato con:

```
======================================================================================================
RANK   SEARCH TERM                    CPC        COST       CLICKS   CONV     SCORE
======================================================================================================
1      expensive keyword here         $15.50     $465.00    30       0.0      1545.00
2      another bad term              $12.30     $246.00    20       0.0      1254.30
...
```

### Interpretazione dei Risultati

- **CPC**: Costo medio per click
- **COST**: Costo totale speso per questo termine
- **CLICKS**: Numero di click ricevuti
- **CONV**: Numero di conversioni generate
- **SCORE**: Punteggio di "negatività" (più alto = peggiore)

### Come Funziona il Badness Score

Il punteggio viene calcolato considerando:
- **30%** - CPC alto: Termini con costo per click elevato
- **40%** - Tasso di conversione basso: Termini con poche o zero conversioni
- **30%** - Spreco di budget: Costo speso senza generare conversioni

## Prossimi Passi

Dopo aver identificato i peggiori termini:

1. **Rivedi i termini**: Controlla se sono rilevanti per il tuo business
2. **Aggiungi come keyword negative**: Considera l'aggiunta di questi termini come negative keywords
3. **Ottimizza le campagne**: Usa questi insight per migliorare il targeting
4. **Monitora regolarmente**: Esegui l'analisi periodicamente per mantenere ottimizzate le campagne

## Risoluzione Problemi

### Errore di autenticazione
```
Error fetching search terms: Request failed with status code 401
```
**Soluzione**: Verifica che le credenziali nel file `google-ads.yaml` siano corrette e che il refresh token non sia scaduto.

### Customer ID non valido
```
Error: Customer ID must contain only digits
```
**Soluzione**: Assicurati di inserire solo i numeri del customer ID, senza trattini (es. `1234567890` invece di `123-456-7890`).

### Nessun termine trovato
```
No search terms found.
```
**Soluzione**: Potrebbe non esserci dati per il periodo specificato. Prova ad aumentare il numero di giorni con `--days 60`.

## Licenza

MIT License

## Contributi

I contributi sono benvenuti! Sentiti libero di aprire issue o pull request.

## Supporto

Per domande o problemi, apri un issue su GitHub.
