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

### Quick Setup (Recommended)

The easiest way to set up the project is using the provided setup script, which automatically creates a virtual environment and installs all dependencies:

**Linux/macOS:**
```bash
git clone https://github.com/red093/gads-search-terms-exclusion.git
cd gads-search-terms-exclusion
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
git clone https://github.com/red093/gads-search-terms-exclusion.git
cd gads-search-terms-exclusion
setup.bat
```

The setup script will:
- ✅ Check Python version (3.7+ required)
- ✅ Create a virtual environment (isolates dependencies)
- ✅ Install all required packages
- ✅ Optionally copy the config template

### Manual Installation

If you prefer to set up manually:

1. Clone the repository:
```bash
git clone https://github.com/red093/gads-search-terms-exclusion.git
cd gads-search-terms-exclusion
```

2. Create and activate a virtual environment:
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Why Use a Virtual Environment?

A virtual environment:
- 🔒 Isolates project dependencies from system Python
- ✅ Prevents version conflicts with other projects
- 📦 Makes the project reproducible across different machines
- 🧹 Keeps your system Python clean

### Configure Google Ads API Credentials

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

   **Step 2a: Create OAuth2 Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the **Google Ads API** (search in API Library)
   - Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
   - Choose **Desktop app** as application type
   - Download the credentials (you'll get client_id and client_secret)

   **Step 2b: Generate Refresh Token**

   Use the included helper script to generate your refresh token:

   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

   # Run the token generator
   python generate_refresh_token.py
   ```

   The script will:
   - Prompt you for your Client ID and Client Secret
   - Open a browser window for you to authorize the app
   - Display your refresh token (save this in google-ads.yaml)

   **Alternative Method** (if the helper script doesn't work):

   Use Google's OAuth2 Playground:
   1. Go to [OAuth2 Playground](https://developers.google.com/oauthplayground/)
   2. Click the gear icon (⚙️) in the top right
   3. Check "Use your own OAuth credentials"
   4. Enter your Client ID and Client Secret
   5. In Step 1, scroll down and select "Google Ads API v14" → "https://www.googleapis.com/auth/adwords"
   6. Click "Authorize APIs"
   7. Sign in and grant permissions
   8. Click "Exchange authorization code for tokens"
   9. Copy the "Refresh token" value

## MCC (Manager Account) Access

The script supports accessing client accounts through a Google Ads Manager (MCC) account. This is useful for agencies or businesses managing multiple Google Ads accounts.

### Configuration for MCC Access

There are two ways to configure MCC access:

#### Option 1: Using Configuration File

Set the `login_customer_id` in your `google-ads.yaml` to your MCC account ID:

```yaml
login_customer_id: 9876543210  # Your MCC account ID
```

Then run the script with the client account ID:

```bash
python search_terms_analyzer.py --customer-id 1234567890
```

Where:
- `login_customer_id` (in config) = Your MCC manager account ID
- `--customer-id` (command line) = The client account ID you want to analyze

#### Option 2: Using Command Line Parameter

Override the config file by specifying the MCC account on the command line:

```bash
python search_terms_analyzer.py \
    --customer-id 1234567890 \
    --login-customer-id 9876543210
```

This is useful if you:
- Want to use different MCC accounts without editing the config
- Need to quickly switch between manager accounts
- Share the same config file across different scenarios

### MCC Access Requirements

To use MCC access, ensure:
1. Your MCC account has access to the client account
2. The developer token is from the MCC account (or a test account linked to it)
3. The OAuth credentials have been granted permission for the MCC account

## Usage

### Running the Analyzer

#### Option 1: Using the Helper Script (Easiest)

The helper script automatically activates the virtual environment and runs the analyzer:

**Linux/macOS:**
```bash
./run.sh --customer-id YOUR_CUSTOMER_ID
```

**Windows:**
```cmd
run.bat --customer-id YOUR_CUSTOMER_ID
```

#### Option 2: Manual Execution

Activate the virtual environment first, then run the script:

**Linux/macOS:**
```bash
source venv/bin/activate
python search_terms_analyzer.py --customer-id YOUR_CUSTOMER_ID
deactivate  # When done
```

**Windows:**
```cmd
venv\Scripts\activate
python search_terms_analyzer.py --customer-id YOUR_CUSTOMER_ID
deactivate  # When done
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

- `--customer-id`: **(Required)** Google Ads customer ID to analyze (without hyphens)
- `--login-customer-id`: **(Optional)** MCC manager account ID for authentication (without hyphens). Use when accessing client accounts through a manager account.
- `--campaign-id`: **(Optional)** Campaign ID to analyze (can be specified multiple times). If not specified, analyzes all campaigns.
- `--list-campaigns`: List all campaigns in the account and exit
- `--days`: Number of days to analyze (default: 30)
- `--top`: Number of worst terms to display (default: 10)
- `--config`: Path to configuration file (default: google-ads.yaml)
- `--export`: Export results to a CSV file (optional)

## Examples

All examples below use the helper script. If running manually, activate the virtual environment first.

### Analyze last 30 days (default)
```bash
./run.sh --customer-id 1234567890
```

### Analyze last 7 days and show top 20
```bash
./run.sh --customer-id 1234567890 --days 7 --top 20
```

### Export results to CSV
```bash
./run.sh --customer-id 1234567890 --export report.csv
```

### Access client account via MCC (Manager account)
```bash
./run.sh --customer-id 1234567890 --login-customer-id 9876543210
```

### List all campaigns in the account
```bash
./run.sh --customer-id 1234567890 --list-campaigns
```

This will display all campaigns with their IDs, names, status, and performance metrics.

### Analyze a specific campaign
```bash
./run.sh --customer-id 1234567890 --campaign-id 987654321
```

### Analyze multiple campaigns
```bash
./run.sh --customer-id 1234567890 --campaign-id 987654321 --campaign-id 123456789
```

### Analyze specific campaign with custom date range
```bash
./run.sh --customer-id 1234567890 --campaign-id 987654321 --days 14 --top 20
```

**Note:** On Windows, use `run.bat` instead of `./run.sh`

## Output

The script produces a formatted report with:

```
==================================================================================================================================
RANK   SEARCH TERM                    CAMPAIGN                  CPC        COST       CLICKS   CONV     SCORE
==================================================================================================================================
1      expensive keyword here         My Campaign Name          $15.50     $465.00    30       0.0      1545.00
2      another bad term              Another Campaign          $12.30     $246.00    20       0.0      1254.30
...
```

### Understanding the Results

- **RANK**: Position in the ranking (1 = worst performing)
- **SEARCH TERM**: The actual search query that triggered your ad
- **CAMPAIGN**: The campaign where this search term appeared
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
