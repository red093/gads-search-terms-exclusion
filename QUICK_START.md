# Quick Start Guide - Google Ads Search Terms Analyzer

## 🚀 Quick Setup (3 minutes)

### Automated Setup (Recommended)

**Linux/macOS:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

The setup script will:
- ✅ Create an isolated virtual environment
- ✅ Install all dependencies automatically
- ✅ Check Python version compatibility
- ✅ Optionally copy the config template

Then configure your credentials:
```bash
nano google-ads.yaml  # or use any text editor
```

And run:
```bash
./run.sh --customer-id YOUR_CUSTOMER_ID
```

### Manual Setup

If you prefer to do it manually:

```bash
# 1. Create virtual environment
python3 -m venv venv            # Linux/macOS
python -m venv venv             # Windows

# 2. Activate it
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
cp google-ads.yaml.example google-ads.yaml
# Edit google-ads.yaml with your credentials

# 5. Run the analyzer
python search_terms_analyzer.py --customer-id YOUR_CUSTOMER_ID
```

## 📋 Obtaining Google Ads Credentials

### Developer Token
1. Log in to [Google Ads](https://ads.google.com/)
2. Go to **Tools and Settings** → **API Center**
3. Request a developer token

### OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Ads API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Application type: **Desktop application**
6. Download the credentials (client_id and client_secret)

### Generate Refresh Token

Run this command with your client_id and client_secret:

```bash
python -m google.ads.googleads.oauth2.generate_refresh_token \
    --client_id YOUR_CLIENT_ID \
    --client_secret YOUR_CLIENT_SECRET
```

Follow the instructions to authorize the app and obtain the refresh_token.

## 🏢 MCC (Manager Account) Access

If you're an agency or manage multiple accounts through a Google Ads Manager (MCC) account:

1. Set `login_customer_id` in `google-ads.yaml` to your **MCC account ID**
2. Use `--customer-id` with the **client account ID** you want to analyze

Example:
```bash
# MCC account: 9876543210
# Client account: 1234567890
./run.sh --customer-id 1234567890
```

Or override via command line:
```bash
./run.sh --customer-id 1234567890 --login-customer-id 9876543210
```

## 💡 Usage Examples

**Note:** Examples use `./run.sh` (Linux/macOS) or `run.bat` (Windows)

### Standard analysis (last 30 days)
```bash
./run.sh --customer-id 1234567890
```

### Analyze last 7 days
```bash
./run.sh --customer-id 1234567890 --days 7
```

### Show top 20 worst terms
```bash
./run.sh --customer-id 1234567890 --top 20
```

### Export to CSV
```bash
./run.sh --customer-id 1234567890 --export report.csv
```

## 📊 Interpreting Results

The script identifies the worst terms based on:

- **High CPC**: Terms that cost a lot per click
- **Low Conversions**: Terms that don't convert
- **Budget Waste**: Cost spent without results

### Example Output:
```
RANK  SEARCH TERM              CPC      COST      CLICKS  CONV   SCORE
1     expensive keyword        $15.50   $465.00   30      0.0    1545.00
2     another useless term     $12.30   $246.00   20      0.0    1254.30
```

## ✅ What to Do with the Results

1. **Review** each term to understand if it's relevant
2. **Add negative keywords** for non-relevant terms
3. **Optimize** campaigns by eliminating waste
4. **Monitor** regularly to maintain performance

## ❓ Common Issues

### "Error 401: Unauthorized"
→ Check that the credentials in `google-ads.yaml` are correct

### "No search terms found"
→ Try a longer period: `--days 60`

### "Customer ID must contain only digits"
→ Use only numbers: `1234567890` (no hyphens: ~~123-456-7890~~)

## 🔐 Security

**IMPORTANT**: The `google-ads.yaml` file contains sensitive credentials!
- ✅ It's already in `.gitignore`
- ❌ NEVER commit it to Git
- ❌ NEVER share it with anyone

---

**Need help?** Open an issue on GitHub!
