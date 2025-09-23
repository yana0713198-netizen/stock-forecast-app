import React from "react";

export default function StockSelector({ ticker, setTicker }) {
  return (
    <div>
      <label>Stock Ticker:</label>
      <input
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
      />
    </div>
  );
}
