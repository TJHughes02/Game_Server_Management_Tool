// Start/Stop/Restart buttons (global)

// DO NOT PLACE BUTTONS IN CREATE

import { useState } from "react";
import { startServer, stopServer, restartServer, deleteServer } from "@/features/api.js";
import { useNavigate } from "react-router-dom";

export default function ServerActions({ server, onChange, onDeleted }) {
  const nav = useNavigate();
  const [busy, setBusy] = useState(false);

  async function handleDelete() {
    if (busy) return;
    if (!window.confirm(`Delete “${server.name}”? This cannot be undone.`)) return;
    setBusy(true);
    try {
      await deleteServer(server.id);
      onChange?.();
      // go to dash after delete
      onDeleted ? onDeleted() : nav("/dashboard");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="actions-row" style={{ display:"flex", gap:8 }}>
      <button
        className="btn small"
        onClick={() => run(() => startServer(server.id))}
        disabled={busy || String(server.status).toLowerCase() === "online"}
        title="Start server"
      >
        Start
      </button>

      <button
        className="btn small"
        onClick={() => run(() => stopServer(server.id), "Stop this server now?")}
        disabled={busy || String(server.status).toLowerCase() === "offline"}
        title="Stop server"
      >
        Stop
      </button>

      <button
        className="btn small"
        onClick={() => run(() => restartServer(server.id), "Restart this server now?")}
        disabled={busy}
        title="Restart server"
      >
        Restart
      </button>

      <button
        className="btn small danger"
        onClick={() => handleDelete(
          async () => { await deleteServer(server.id); onDeleted?.() },
          `Delete “${server.name}”? This cannot be undone.`
        )}
        disabled={busy}
        title="Delete server"
      >
        Delete
      </button>
    </div>
  );
}
