import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
stock_endpoint = os.getenv("STOCK_ENDPOINT")
stock_api_key = os.getenv("STOCK_API_KEY")
news_endpoint = os.getenv("NEWS_ENDPOINT")
news_api_key = os.getenv("NEWS_API_KEY")
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

# Validate all required environment variables
required_vars = {
    "STOCK_ENDPOINT": stock_endpoint,
    "STOCK_API_KEY": stock_api_key,
    "NEWS_ENDPOINT": news_endpoint,
    "NEWS_API_KEY": news_api_key,
    "SENDER_EMAIL": sender_email,
    "RECEIVER_EMAIL": receiver_email,
    "SENDER_PASSWORD": sender_password,
}

missing_vars = [var for var, value in required_vars.items() if value is None]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# List of stocks to monitor
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

# Process each stock in the list
for stock_name, stock_company in STOCKS.items():
    print(f"\nProcessing stock: {stock_name} - {stock_company}")
    
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_name,
        "apikey": stock_api_key
    }

    try:
        response = requests.get(url=stock_endpoint, params=stock_params)
        response.raise_for_status()
        data = response.json().get("Time Series (Daily)", {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock data for {stock_name}: {e}")
        continue
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        continue
    else:
        data_list = [value for (key, value) in data.items()]
        if len(data_list) < 2:
            print(f"Not enough data for {stock_name}")
            continue

        # Get yesterday's closing stock price
        yesterday_data = data_list[0]
        yesterday_closing_price = float(yesterday_data["4. close"])

        # Get the day before yesterday's closing stock price
        day_before_yesterday_data = data_list[1]
        day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

        # Find the positive difference
        difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)

        # Determine if the price is up or down
        up_down = None
        if yesterday_closing_price > day_before_yesterday_closing_price:
            up_down = "🔼"
        else:
            up_down = "🔽"

        # Work out the percentage difference
        diff_percent = round((difference / yesterday_closing_price) * 100, 2)

        # If percentage is greater than 5 then get news
        if abs(diff_percent) > 5:
            print(f"Getting news for {stock_name}")
            news_params = {
                "q": stock_company,
            }
            news_headers = {
                "X-Api-Key": news_api_key
            }
            try:
                news_response = requests.get(news_endpoint, params=news_params, headers=news_headers)
                news_response.raise_for_status()
                articles = news_response.json()["articles"]
            except requests.exceptions.RequestException as e:
                print(f"Error fetching news for {stock_name}: {e}")
                continue
            except ValueError as e:
                print(f"Error parsing JSON response: {e}")
                continue
            else:
                # Get the first 3 articles
                three_articles = articles[:3]

                # Create email body with formatted articles
                email_body = f"{stock_name}: {up_down}{diff_percent}%\n\n"
                email_body += "=" * 50 + "\n\n"
                
                for i, article in enumerate(three_articles, 1):
                    email_body += f"Article {i}:\n"
                    email_body += f"Headline: {article['title']}\n"
                    email_body += f"Brief: {article.get('description', 'No description available')}\n"
                    if article.get('url'):
                        email_body += f"Link: {article['url']}\n"
                    email_body += "\n" + "-" * 50 + "\n\n"

                # Send Email with proper formatting
                try:
                    # Create message
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    msg['Subject'] = f"{stock_name} Stock Alert: {up_down}{diff_percent}%"
                    
                    # Attach body to email
                    msg.attach(MIMEText(email_body, 'plain'))
                    
                    # Send email
                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(user=sender_email, password=sender_password)
                        connection.send_message(msg)
                    
                    print(f"Email sent successfully for {stock_name}")
                except smtplib.SMTPAuthenticationError as e:
                    print(f"SMTP authentication failed: {e}")
                    print("Note: For Gmail, you may need to use an 'App Password' instead of your regular password")
                except smtplib.SMTPException as e:
                    print(f"SMTP error occurred: {e}")
                except Exception as e:
                    print(f"Unexpected error sending email: {e}")
        else:
            print(f"{stock_name}: {up_down}{diff_percent}% - No significant change (threshold: 5%)")

