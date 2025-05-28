# Stock News Monitor

A Python application that monitors stock price changes and sends relevant news alerts via SMS when significant price movements are detected. This application helps investors stay informed about their stocks by automatically tracking price changes and delivering related news articles.

## Features

- Real-time stock price monitoring using Alpha Vantage API
- Automatic news article fetching from News API
- SMS notifications via Twilio
- Price change percentage calculation
- Support for multiple stocks (configurable)
- Daily price comparison
- Top 3 relevant news articles delivery

## Requirements

- Python 3.x
- Required Python packages:
  - requests
  - twilio

## Installation

1. Clone this repository:

```bash
git clone https://github.com/momed-ali01/stock-news.git
cd stock-news
```

2. Install required packages:

```bash
pip install requests twilio
```

3. Configure API keys:
   - Alpha Vantage API key
   - News API key
   - Twilio Account SID and Auth Token

## Configuration

The application requires the following API keys to be configured:

1. Alpha Vantage API key for stock data
2. News API key for news articles
3. Twilio credentials for SMS notifications

You can obtain these keys from:

- Alpha Vantage: https://www.alphavantage.co/
- News API: https://newsapi.org/
- Twilio: https://www.twilio.com/

## Usage

1. Configure your API keys in the main.py file:

```python
STOCK_API_KEY = "your_alpha_vantage_api_key"
NEWS_API_KEY = "your_news_api_key"
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
```

2. Set your target stock and company:

```python
STOCK_NAME = "TSLA"  # Stock symbol
COMPANY_NAME = "Tesla Inc"  # Company name
```

3. Run the application:

```bash
python main.py
```

## How It Works

1. The application fetches daily stock data from Alpha Vantage API
2. Calculates the price difference between yesterday and the day before
3. If the price change exceeds 5%, it triggers a news search
4. Fetches the top 3 relevant news articles about the company
5. Sends SMS notifications with:
   - Stock symbol and price change percentage
   - Article headlines
   - Brief article descriptions

## Message Format

The SMS notifications are formatted as follows:

```
TSLA: 🔺2%
Headline: [Article Title]
Brief: [Article Description]
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Note

Never commit your API keys to version control. Consider using environment variables or a configuration file for sensitive credentials.
