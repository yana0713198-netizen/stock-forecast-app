from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
from typing import List, Optional
from utils.forecast import predict_stock
from utils.news import fetch_news
from utils.sentiment import analyze_sentiment
import pandas as pd
from io import StringIO
import os
from dotenv import load_dotenv

load_dotenv()  
print("DEBUG: NEWSAPI_KEY =", os.getenv("NEWSAPI_KEY"))



app = FastAPI()

# CORS設定追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    ticker: str
    news_keywords: Optional[List[str]] = []
    free_text: Optional[str] = ""
    model: str = "prophet"

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/predict/")
async def predict(
    ticker: str = Form(...),
    news_keywords: str = Form(""),
    free_text: str = Form(""),
    model: str = Form("prophet"),
    file: UploadFile = File(None)
):
    # ファイルがあれば読み込む
    df_file = None
    if file:
        df_file = pd.read_csv(StringIO(file.file.read().decode()))

    # 株価予測
    forecast = predict_stock(ticker, model, df_file)

    # ニュース取得
    keywords = news_keywords.split(",") if news_keywords else []
    news_list = fetch_news(ticker, keywords, free_text)

    # 感情分析
    sentiments = analyze_sentiment([n['title'] for n in news_list])

    return {
        "forecast": forecast,
        "news": news_list,
        "sentiments": sentiments
    }
