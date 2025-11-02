from db_connection import get_db

db = get_db()
news_col = db['news']
stocks_col = db['stocks']

# --- Count number of headlines per sentiment ---
def count_headlines_by_sentiment():
    pipeline = [
        {
            "$group": {
                "_id": "$sentiment",
                "count": {"$sum": 1}
            }
        }
    ]
    results = news_col.aggregate(pipeline)
    for result in results:
        print(f"Sentiment: {result['_id']}, Count: {result['count']}")


# --- Count average sentiment score per stock ---
def count_avg_sentiment_by_stock():
    pipeline = [
        {
            "$group": {
                "_id": "$symbol",
                "avg_sentiment": {"$avg": "$sentiment_score"}
            }
        },
        {
            "$sort": {"avg_sentiment": -1}
        }
    ]
    results = news_col.aggregate(pipeline)
    for result in results:
        print(f"Stock: {result['_id']}, Average Sentiment: {result['avg_sentiment']}")  

# --- Top Positive Headlines ---    
def top_positive_headlines(limit=5):
    
    for doc in news_col.find({}, {"_id": 0, "title": 1, "sentiment_label": 1, "sentiment_score": 1}).sort("sentiment_score", -1).limit(5):
        print(doc)



if __name__ == "__main__":
    count_headlines_by_sentiment()
    #count_avg_sentiment_by_stock()
    print("\nTop Positive Headlines:")
    top_positive_headlines()