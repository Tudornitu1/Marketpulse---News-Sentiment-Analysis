from dotenv import load_dotenv
import os
import pymongo
import certifi
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests


load_dotenv()   

MONGODB_URI = os.getenv("MONGODB_URI")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

client = pymongo.MongoClient(MONGODB_URI, tlsCAFile=certifi.where())

db = client['marketpulse_db']
news_col = db['news']
stocks_col = db['stocks']

def get_company_news(symbol, query=None, days=7):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={symbol}"
        f"{'+' + query if query else ''}&"
        f"from={start_date.strftime('%Y-%m-%d')}&"
        f"to={end_date.strftime('%Y-%m-%d')}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        print(f"Error fetching news: {data.get('message')}")
        return pd.DataFrame()   

    articles = data.get("articles", [])
    df = pd.DataFrame([{
        "symbol": symbol,
        "title": article["title"],
        "description": article["description"],
        "url": article["url"],
        "date": article["publishedAt"],
        "source": article["source"]["name"]
    } for article in articles if article["title"]])

    return df

def insert_news_article(article):
    news_col.insert_one(article)

def insert_stock_data(stock_data):
    stocks_col.insert_one(stock_data)

if __name__ == "__main__":
    """ tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'DIS']

    def _flatten(col):
        if isinstance(col, tuple):
            parts = [str(p) for p in col if p is not None and p != ""]
            return "_".join(parts) if parts else ""
        return str(col)

    for t in tickers:
        df = yf.download(t, start="2024-01-01", end="2025-10-01")
        if df.empty:
            print(f"No data for {t}, skipping.")
            continue

        df = df.copy()
        df.columns = [_flatten(c) for c in df.columns]
        records_df = df.reset_index()

        if 'Date' in records_df.columns:
            records_df['Date'] = records_df['Date'].apply(lambda x: x.to_pydatetime() if hasattr(x, "to_pydatetime") else x)

        records = records_df.to_dict(orient='records')
        for r in records:
            r['symbol'] = t
            insert_stock_data(r)

        print(f"Inserted {len(records)} records for {t}.")

    print("Stock data inserted successfully.")  """

    companies = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'DIS']
    for symbol in companies:
        news_df = get_company_news(symbol, days=7)
        print(f"Fetched {len(news_df)} news articles for {symbol}.")
        for _, row in news_df.iterrows():
            article = row.to_dict()
            insert_news_article(article)
    print("News articles inserted successfully.")
    
    client.close()