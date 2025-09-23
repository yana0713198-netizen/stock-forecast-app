import React from "react";

export default function NewsPanel({ news }) {
  return (
    <div>
      <h3>News</h3>
      <ul>
        {news.map((n, idx) => (
          <li key={idx}>{n.title}</li>
        ))}
      </ul>
    </div>
  );
}
