# Stock News Monitor

An automated stock monitoring service that tracks price changes for multiple stocks and sends relevant news alerts via email when significant price movements are detected. This project uses Python to fetch stock data from Alpha Vantage API, retrieves related news articles from News API, and sends formatted email notifications using Gmail SMTP.

## Features

- **Multi-stock monitoring**: Monitor multiple stocks simultaneously (TSLA, AAPL, GOOG, AMZN, META, IBM, INTC, NVDA, MSFT, and more)
- **API-based stock data fetching** from Alpha Vantage
- **Automatic news article retrieval** from News API
- **Email delivery system** via Gmail SMTP with formatted messages
- **Price change detection** with 5% threshold for alerts
- **Environment variable configuration** for secure credential management
- **Comprehensive error handling** for API and email operations
- **Easy to automate** with task schedulers

## Requirements

- Python 3.x
- Gmail account with App Password enabled
- API access:
  - Alpha Vantage API key (free tier available)
  - News API key (free tier available)
- Required Python packages (see `requirements.txt`):
  - `python-dotenv` - For loading environment variables
  - `requests` - For making API calls to fetch stock data and news articles
  - `smtplib` - Built into Python standard library for email sending
  - `email.mime` - Built into Python standard library for email formatting

## Installation

1. Clone this repository:

```bash
git clone https://github.com/<username>/stock-news.git
cd stock-news
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate # On Windows
source venv/bin/activate # On macOS/Linux
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:

```env
STOCK_ENDPOINT=https://www.alphavantage.co/query
STOCK_API_KEY=your_alpha_vantage_api_key
NEWS_ENDPOINT=https://newsapi.org/v2/everything
NEWS_API_KEY=your_news_api_key
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=recipient@example.com
SENDER_PASSWORD=your_gmail_app_password
```

**Important:**

- Replace all placeholder values with your actual credentials
- Never commit the `.env` file to version control
- For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password
- Enable 2-Factor Authentication in your Google Account before generating an App Password

## Configuration

### API Keys

1. **Alpha Vantage API Key**:
   - Sign up at: https://www.alphavantage.co/
   - Free tier available (500 API calls per day)
   - Copy your API key and add it to `.env` as `STOCK_API_KEY`

2. **News API Key**:
   - Sign up at: https://newsapi.org/
   - Free tier available (100 requests per day)
   - Copy your API key and add it to `.env` as `NEWS_API_KEY`

### Stock Configuration

Edit the `STOCKS` dictionary in `main.py` to add or remove stocks you want to monitor:

```python
STOCKS = {
    "TSLA": "Tesla Inc",
    "AAPL": "Apple Inc",
    "GOOG": "Alphabet Inc",
    "AMZN": "Amazon.com Inc",
    "META": "Meta Platforms Inc",
    "IBM": "IBM Corporation",
    "INTC": "Intel Corporation",
    "NVDA": "NVIDIA Corporation",
    "MSFT": "Microsoft Corporation",
    # Add more stocks as needed
}
```

## Usage

To run the script:

```bash
python main.py
```

### How It Works

1. The script loads environment variables from `.env` file
2. Validates that all required environment variables are present
3. Iterates through each stock in the `STOCKS` dictionary
4. For each stock:
   - Fetches daily stock data from Alpha Vantage API
   - Calculates the price difference between yesterday's and the day before yesterday's closing prices
   - Determines if the price went up (🔼) or down (🔽)
   - Calculates the percentage change
   - If the change exceeds 5% (up or down):
     - Fetches the top 3 relevant news articles from News API
     - Formats the articles with stock symbol, percentage change, headlines, descriptions, and links
     - Sends a formatted email alert via Gmail SMTP
   - Displays progress and results in the console

### Email Format

The email notifications include:

- **Subject**: `{STOCK_SYMBOL} Stock Alert: {INDICATOR}{PERCENTAGE}%`
- **Body**: Formatted with stock symbol, percentage change, and top 3 articles:

```
TSLA: 🔼5.23%

==================================================

Article 1:
Headline: [Article Title]
Brief: [Article Description]
Link: [Article URL]

--------------------------------------------------

Article 2:
Headline: [Article Title]
Brief: [Article Description]
Link: [Article URL]

--------------------------------------------------

Article 3:
Headline: [Article Title]
Brief: [Article Description]
Link: [Article URL]

--------------------------------------------------
```

### Error Handling

The script includes comprehensive error handling for:

- Missing environment variables (raises ValueError with list of missing variables)
- API request failures (network errors, timeouts, HTTP errors)
- JSON parsing errors
- Insufficient stock data (less than 2 days of data)
- SMTP authentication failures
- General SMTP errors
- Unexpected exceptions

Errors are logged to the console and the application continues processing other stocks even if one fails.

## Setting Up Automated Execution

To run this script automatically on a schedule, you can:

1. **Windows Task Scheduler**: Create a scheduled task to run the script daily (recommended: once per day after market close)
2. **Linux/Mac Cron Jobs**: Add a cron job to execute the script at specified intervals
3. **Cloud Services**: Deploy to AWS Lambda, Google Cloud Functions, or similar services
4. **GitHub Actions**: Set up a scheduled workflow to run the script

Example cron job (runs daily at 4:30 PM, after market close):

```bash
30 16 * * * /usr/bin/python3 /path/to/stock-news/main.py
```

**Note**: The script checks yesterday's closing price, so it's best to run it after the market closes (typically 4:00 PM EST) or the next morning.

## Security Notes

- **Never commit your `.env` file** to version control - it contains sensitive credentials
- The `.env` file is already included in `.gitignore` to prevent accidental commits
- Use Gmail's App Passwords instead of your main account password
- Keep your API keys secure and rotate them periodically if compromised
- Consider using a secrets management service for production deployments
- Be aware of API rate limits (Alpha Vantage: 500 calls/day, News API: 100 calls/day on free tier)
- Monitor your API usage to avoid exceeding limits

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is for educational purposes.
