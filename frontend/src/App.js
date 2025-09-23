import React, { useState } from "react";
import StockSelector from "./components/StockSelector";
import NewsPanel from "./components/NewsPanel";
import FileUpload from "./components/FileUpload";
import ModelSelector from "./components/ModelSelector";
import ForecastChart from "./components/ForecastChart";  // ← 追加

function App() {
  const [ticker, setTicker] = useState("");
  const [news, setNews] = useState([]);
  const [forecast, setForecast] = useState([]);
  const [file, setFile] = useState(null);
  const [model, setModel] = useState("prophet");

  const handlePredict = async () => {
    const formData = new FormData();
    formData.append("ticker", ticker);
    formData.append("model", model);
    if (file) formData.append("file", file);

    const resp = await fetch("http://localhost:8000/predict/", {
      method: "POST",
      body: formData,
    });
    const data = await resp.json();

    // ★ここで中身を確認
    console.log("API response:", data);
    console.log("Forecast length:", data.forecast?.length || 0);
    if (data.forecast && data.forecast.length > 0) {
      console.log("First forecast element:", data.forecast[0]);
    } else {
      console.warn("⚠️ forecast is empty!");
    }

    setForecast(data.forecast || []);
    setNews(data.news || []);
  };

  return (
    <div>
      <StockSelector ticker={ticker} setTicker={setTicker} />
      <FileUpload file={file} setFile={setFile} />
      <ModelSelector model={model} setModel={setModel} />
      <button onClick={handlePredict}>Predict</button>
      <NewsPanel news={news} />
      <div>
        <h3>Forecast</h3>
        {/* 折れ線チャート追加 */}
        {forecast.length > 0 && <ForecastChart forecast={forecast} />}

        {/* リスト表示 */}
        <ul>
          {forecast.map((f, idx) => (
            <li key={idx}>
              {f.ds ? new Date(String(f.ds)).toLocaleDateString("ja-JP") : "N/A"} :
              {f.yhat !== undefined ? Number(f.yhat).toFixed(2) : "N/A"}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
