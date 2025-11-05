# Google Ads Search Terms Analyzer

Python script to analyze search terms from a Google Ads account and identify the worst performers based on high CPC and low conversions.

## Features

- 🔍 Analyzes search terms from Google Ads account
- 📊 Identifies the 10 worst performing terms based on:
  - Highest CPC (Cost Per Click)
  - Lowest number of conversions
  - Total cost spent without conversions
- 📈 Calculates a "badness score" for each term
- 💾 Exports results to CSV format
- ⚙️ Configurable for different analysis periods

## Prerequisites

- Python 3.7 or higher
- Google Ads account with API access
- Google Ads API credentials configured

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gads-search-terms-exclusion
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Google Ads API credentials:

Create a `google-ads.yaml` file in the project directory with your credentials:

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
login_customer_id: YOUR_LOGIN_CUSTOMER_ID
use_proto_plus: True
```

### How to Obtain API Credentials

1. **Developer Token**: Get it from your Google Ads Manager account
   - Go to Tools & Settings > API Center
   - Request a developer token

2. **OAuth2 Credentials** (client_id, client_secret, refresh_token):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Ads API
   - Create OAuth 2.0 credentials
   - Generate a refresh token using the Google Ads authentication script

To generate the refresh token:
```bash
python -m google.ads.googleads.oauth2.generate_refresh_token \
    --client_id YOUR_CLIENT_ID \
    --client_secret YOUR_CLIENT_SECRET
```

## Usage

### Basic Command

```bash
python search_terms_analyzer.py --customer-id YOUR_CUSTOMER_ID
```

### Advanced Options

```bash
python search_terms_analyzer.py \
    --customer-id 1234567890 \
    --days 30 \
    --top 10 \
    --config google-ads.yaml \
    --export results.csv
```

### Parameters

- `--customer-id`: **(Required)** Google Ads customer ID (without hyphens)
- `--days`: Number of days to analyze (default: 30)
- `--top`: Number of worst terms to display (default: 10)
- `--config`: Path to configuration file (default: google-ads.yaml)
- `--export`: Export results to a CSV file (optional)

## Examples

### Analyze last 30 days (default)
```bash
python search_terms_analyzer.py --customer-id 1234567890
```

### Analyze last 7 days and show top 20
```bash
python search_terms_analyzer.py --customer-id 1234567890 --days 7 --top 20
```

### Export results to CSV
```bash
python search_terms_analyzer.py --customer-id 1234567890 --export report.csv
```

## Output

The script produces a formatted report with:

```
======================================================================================================
RANK   SEARCH TERM                    CPC        COST       CLICKS   CONV     SCORE
======================================================================================================
1      expensive keyword here         $15.50     $465.00    30       0.0      1545.00
2      another bad term              $12.30     $246.00    20       0.0      1254.30
...
```

### Understanding the Results

- **CPC**: Average cost per click
- **COST**: Total cost spent on this term
- **CLICKS**: Number of clicks received
- **CONV**: Number of conversions generated
- **SCORE**: "Badness" score (higher = worse)

### How the Badness Score Works

The score is calculated considering:
- **30%** - High CPC: Terms with elevated cost per click
- **40%** - Low conversion rate: Terms with few or zero conversions
- **30%** - Budget waste: Cost spent without generating conversions

## Next Steps

After identifying the worst performing terms:

1. **Review the terms**: Check if they are relevant to your business
2. **Add as negative keywords**: Consider adding these terms as negative keywords
3. **Optimize campaigns**: Use these insights to improve targeting
4. **Monitor regularly**: Run the analysis periodically to maintain optimized campaigns

## Troubleshooting

### Authentication error
```
Error fetching search terms: Request failed with status code 401
```
**Solution**: Verify that the credentials in the `google-ads.yaml` file are correct and that the refresh token has not expired.

### Invalid Customer ID
```
Error: Customer ID must contain only digits
```
**Solution**: Make sure to enter only the numbers of the customer ID, without hyphens (e.g., `1234567890` instead of `123-456-7890`).

### No terms found
```
No search terms found.
```
**Solution**: There may be no data for the specified period. Try increasing the number of days with `--days 60`.

## License

MIT License

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.

## Support

For questions or problems, open an issue on GitHub.
