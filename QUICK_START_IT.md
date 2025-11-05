# Guida Rapida - Google Ads Search Terms Analyzer

## 🚀 Setup Veloce (5 minuti)

### 1. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 2. Configura le credenziali

Copia il file di esempio:
```bash
cp google-ads.yaml.example google-ads.yaml
```

Modifica `google-ads.yaml` con le tue credenziali Google Ads.

### 3. Esegui l'analisi
```bash
python search_terms_analyzer.py --customer-id TUO_CUSTOMER_ID
```

## 📋 Ottenere le Credenziali Google Ads

### Developer Token
1. Accedi a [Google Ads](https://ads.google.com/)
2. Vai su **Strumenti e impostazioni** → **Centro API**
3. Richiedi un developer token

### OAuth2 Credentials

1. Vai su [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto
3. Abilita **Google Ads API**
4. Vai su **Credenziali** → **Crea credenziali** → **ID client OAuth 2.0**
5. Tipo applicazione: **Applicazione desktop**
6. Scarica le credenziali (client_id e client_secret)

### Genera Refresh Token

Esegui questo comando con i tuoi client_id e client_secret:

```bash
python -m google.ads.googleads.oauth2.generate_refresh_token \
    --client_id TUO_CLIENT_ID \
    --client_secret TUO_CLIENT_SECRET
```

Segui le istruzioni per autorizzare l'app e ottenere il refresh_token.

## 💡 Esempi d'Uso

### Analisi standard (ultimi 30 giorni)
```bash
python search_terms_analyzer.py --customer-id 1234567890
```

### Analisi ultimi 7 giorni
```bash
python search_terms_analyzer.py --customer-id 1234567890 --days 7
```

### Mostra i top 20 peggiori termini
```bash
python search_terms_analyzer.py --customer-id 1234567890 --top 20
```

### Esporta in CSV
```bash
python search_terms_analyzer.py --customer-id 1234567890 --export report.csv
```

## 📊 Interpretazione Risultati

Lo script identifica i termini peggiori basandosi su:

- **CPC Alto**: Termini che costano molto per click
- **Basse Conversioni**: Termini che non convertono
- **Spreco Budget**: Costo speso senza risultati

### Esempio Output:
```
RANK  SEARCH TERM              CPC      COST      CLICKS  CONV   SCORE
1     keyword costoso          $15.50   $465.00   30      0.0    1545.00
2     altro termine inutile    $12.30   $246.00   20      0.0    1254.30
```

## ✅ Cosa Fare con i Risultati

1. **Rivedi** ogni termine per capire se è rilevante
2. **Aggiungi negative keywords** per i termini non pertinenti
3. **Ottimizza** le campagne eliminando lo spreco
4. **Monitora** regolarmente per mantenere le performance

## ❓ Problemi Comuni

### "Error 401: Unauthorized"
→ Controlla che le credenziali in `google-ads.yaml` siano corrette

### "No search terms found"
→ Prova con un periodo più lungo: `--days 60`

### "Customer ID must contain only digits"
→ Usa solo numeri: `1234567890` (no trattini: ~~123-456-7890~~)

## 🔐 Sicurezza

**IMPORTANTE**: Il file `google-ads.yaml` contiene credenziali sensibili!
- ✅ È già nel `.gitignore`
- ❌ NON commitarlo mai su Git
- ❌ NON condividerlo con nessuno

---

**Hai bisogno di aiuto?** Apri un issue su GitHub!
