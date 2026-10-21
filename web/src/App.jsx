import { useEffect, useState } from "react";

export default function App() {
  const [health, setHealth] = useState("…");

  useEffect(() => {
    fetch("/api/v1/health")
      .then((r) => r.json())
      .then((d) => setHealth(`API ${d.status} · DB ${d.db}`))
      .catch(() => setHealth("API injoignable"));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: "3rem", color: "#111" }}>
      <h1 style={{ margin: 0 }}>Veda</h1>
      <p style={{ marginTop: "0.5rem", color: "#333" }}>
        Dépôts financiers vérifiés — coquille technique.
      </p>
      <p style={{ marginTop: "1.5rem", color: "#555" }}>{health}</p>
    </main>
  );
}
