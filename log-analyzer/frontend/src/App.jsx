import { useState } from "react";
import axios from "axios";

import StatusChart from "./components/StatusChart";
import EndpointChart from "./components/EndpointChart";

export default function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://127.0.0.1:8000/upload", formData);
    setData(res.data);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Log Analyzer Dashboard</h2>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Analyze</button>

      {data && (
        <>
          <h3>Summary</h3>
          <p>Total: {data.total}</p>
          <p>Valid: {data.valid}</p>
          <p>Malformed: {data.malformed}</p>

          <div style={{ display: "flex", gap: "40px" }}>
            <StatusChart statusCounts={data.status_counts} />
            <EndpointChart endpointHits={data.endpoint_hits} />
          </div>
        </>
      )}
    </div>
  );
}
