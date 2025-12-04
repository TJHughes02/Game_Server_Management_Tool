import { useEffect, useState } from "react";
import { http } from "@/services/http";

/**
 * Polls the backend logs endpoint for a given server.
 *
 * Returns:
 *   { lines, loading, error }
 */
export function useLogs(serverId, { pollIntervalMs = 2000, maxLines = 200 } = {}) {
  const [lines, setLines] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!serverId) {
      setLines([]);
      return;
    }

    let cancelled = false;
    let timerId = null;

    const fetchLogs = async () => {
      try {
        setLoading(true);
        const res = await http.get(`/api/servers/${serverId}/logs`, {
          params: { lines: maxLines },
        });

        if (cancelled) return;

        const data = res.data || {};
        const newLines = Array.isArray(data.lines) ? data.lines : [];

        // REPLACES NOT APPENDS, APPENDING = BAD
        setLines(newLines);
        setError(null);
      } catch (err) {
        if (cancelled) return;
        setError(err);
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    // Initial fetch
    fetchLogs();
    // Start polling
    timerId = setInterval(fetchLogs, pollIntervalMs);

    return () => {
      cancelled = true;
      if (timerId) {
        clearInterval(timerId);
      }
    };
  }, [serverId, pollIntervalMs, maxLines]);

  return { lines, loading, error };
}
