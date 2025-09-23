// src/components/ForecastChart.jsx
import React from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function ForecastChart({ forecast }) {
  console.log("ForecastChart props:", forecast);

  // 日付を文字列に変換
  const chartData = forecast.map((f) => ({
    ds: f.ds ? new Date(f.ds).toLocaleDateString("ja-JP") : "N/A",
    yhat: f.yhat !== undefined ? Number(f.yhat) : null,
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="ds" />
        <YAxis />
        <Tooltip />
        {/* 数値データだけを描画 */}
        <Line type="monotone" dataKey="yhat" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default ForecastChart;
