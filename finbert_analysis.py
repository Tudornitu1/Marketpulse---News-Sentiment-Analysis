from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import os
import certifi
import pymongo


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client['marketpulse_db']
news_col = db['news']

tqdm.pandas()


tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

labels = ['positive', 'negative', 'neutral']

def analyze_sentiment(text):
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        scores = outputs.logits[0].numpy()
        scores = np.exp(scores) / np.sum(np.exp(scores))
        sentiment = labels[np.argmax(scores)]
        return sentiment, scores
    except Exception as e:
        print(f"Error analyzing sentiment for text: {text}. Error: {e}")
        return 'neutral', [0.0, 1.0, 0.0]

    tqdm.pandas()
    df['sentiment_analysis'] = df['title'].progress_apply(analyze_sentiment)
    df[['sentiment', 'sentiment_scores']] = pd.DataFrame(df['sentiment_analysis'].tolist(), index=df.index)
    df.drop(columns=['sentiment_analysis'], inplace=True)
    return df
def analyze_text_sentiment(text):
    """Analyze a single text string and return (label, scores_list)."""
    if not isinstance(text, str):
        text = str(text)
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits[0].cpu().numpy()
        # stable softmax
        exp = np.exp(logits - np.max(logits))
        probs = exp / np.sum(exp)
        sentiment = labels[int(np.argmax(probs))]
        return sentiment, probs.tolist()
    except Exception as e:
        print(f"Error analyzing sentiment for text: {text!r}. Error: {e}")
        # return a neutral fallback with zeros-like probs
        fallback = [0.0] * len(labels)
        if len(fallback) >= 2:
            fallback[len(fallback) // 2] = 1.0
        return 'neutral', fallback


def analyze_df(df, text_col='title'):
    """Apply sentiment analysis to a DataFrame column and append 'sentiment' and 'sentiment_scores'."""
    df = df.copy()
    if text_col not in df.columns:
        df[text_col] = ""
    df[text_col] = df[text_col].fillna('').astype(str)
    df['sentiment_analysis'] = df[text_col].progress_apply(analyze_text_sentiment)
    df[['sentiment', 'sentiment_scores']] = pd.DataFrame(df['sentiment_analysis'].tolist(), index=df.index)
    df.drop(columns=['sentiment_analysis'], inplace=True)
    return df


if __name__ == "__main__":
    articles = list(news_col.find({"sentiment": {"$exists": False}}))
    if not articles:
        print("No new articles to analyze.")
    else:
        df = pd.DataFrame(articles)
        print(f"Analyzing sentiment for {len(df)} articles...")
        df = analyze_df(df, text_col='title')
        for _, row in df.iterrows():
            news_col.update_one(
                {"_id": row["_id"]},
                {"$set": {
                    "sentiment": row["sentiment"],
                    "sentiment_scores": row["sentiment_scores"]
                }}
            )
        print("Sentiment analysis completed and updated in the database.")
    client.close()