import React from "react";

export default function ModelSelector({ model, setModel }) {
  return (
    <div>
      <label>Select Model:</label>
      <select value={model} onChange={(e) => setModel(e.target.value)}>
        <option value="prophet">Prophet</option>
        <option value="arima">ARIMA</option>
      </select>
    </div>
  );
}
