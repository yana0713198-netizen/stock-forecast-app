import requests
import os

def fetch_news(ticker: str, keywords=[], free_text=""):
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # ← 関数内で毎回取得
    print("DEBUG: Loaded NEWSAPI_KEY =", NEWSAPI_KEY)

    if not NEWSAPI_KEY:
        print("ERROR: NEWSAPI_KEY is missing or invalid")
        return []

    # クエリ組み立て
    query = f"{ticker} {' '.join(keywords)} {free_text}".strip()
    if not query:
        query = ticker

    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}&pageSize=5"
    print("DEBUG: url =", url)

    try:
        resp = requests.get(url)
        print("DEBUG: status =", resp.status_code)
        data = resp.json()
        print("DEBUG: response =", data)

        if resp.status_code == 200:
            articles = data.get("articles", [])
            return [{"title": a.get("title"), "description": a.get("description")} for a in articles]
        else:
            return []
    except Exception as e:
        print("ERROR: fetch_news failed:", e)
        return []
