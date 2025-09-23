from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(texts):
    return sentiment_pipeline(texts)
