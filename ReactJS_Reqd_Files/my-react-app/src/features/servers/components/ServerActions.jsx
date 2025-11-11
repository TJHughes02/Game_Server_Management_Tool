// Start/Stop/Restart buttons (global)

// DO NOT PLACE BUTTONS IN CREATE

import { useState } from "react";
import { startServer, stopServer, restartServer, deleteServer } from "@/api.js";

export default function ServerActions({ server, onChange, onDeleted }) {
  const [busy, setBusy] = useState(false);

  async function run(fn, confirmText) {
    if (busy) return;
    if (confirmText && !window.confirm(confirmText)) return;
    setBusy(true);
    try {
      await fn();
      onChange?.();
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
        onClick={() => run(
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
