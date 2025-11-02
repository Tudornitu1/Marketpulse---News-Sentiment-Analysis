from db_connection import get_db
from datetime import datetime

db = get_db()
news_col = db['news']
stocks_col = db['stocks']

# --- CREATE ---
def insert_news_article(article):
    result = news_col.insert_one(article)
    print(f"Inserted article with id: {result.inserted_id}")

# --- READ ---
def get_news_article_by_symbol(symbol):
    article = news_col.find_one({"symbol": symbol})
    print(article)

# --- UPDATE ---
def update_news_article_title(symbol, new_title):
    result = news_col.update_one(
        {"symbol": symbol},
        {"$set": {"title": new_title}}
    )
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")

# --- DELETE ---
def delete_news_article_by_symbol(symbol):
    result = news_col.delete_one({"symbol": symbol})
    print(f"Deleted {result.deleted_count} documents.")

if __name__ == "__main__":
    insert_news_article({
        "symbol": "AAPL",
        "title": "Apple Releases New Product",
        "sentiment": "positive",
        "date": "2025-10-01"
    })
    get_news_article_by_symbol("AAPL")
    update_news_article_title("AAPL", "Apple Unveils New iPhone")
    delete_news_article_by_symbol("AAPL")

    
