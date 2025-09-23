import React from "react";

export default function FileUpload({ file, setFile }) {
  return (
    <div>
      <label>Upload CSV:</label>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
    </div>
  );
}
