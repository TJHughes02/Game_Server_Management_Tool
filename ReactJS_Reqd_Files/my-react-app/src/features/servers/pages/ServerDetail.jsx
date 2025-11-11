import { useEffect, useMemo, useRef, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { http } from '@/services/http.js'
import { GAMES } from '@/constants/games.js'
import { deleteServer } from "@/api.js";

function formatDuration(sec) {
  if (!sec || sec <= 0) return '—'
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return [h ? `${h}h` : null, m ? `${m}m` : null, s ? `${s}s` : null].filter(Boolean).join(' ')
}

export default function ServerDetail() {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [tab, setTab] = useState('overview')

  // Console (RCON)
  const [cmd, setCmd] = useState('')
  const [consoleLines, setConsoleLines] = useState([]) // {ts, kind:'in'|'out', text}

  // Logs polling
  const [logs, setLogs] = useState([])
  const [cursor, setCursor] = useState(0)
  const [follow, setFollow] = useState(true)
  const logEndRef = useRef(null)

  const gameLabelByKey = useMemo(
    () => Object.fromEntries(GAMES.map(g => [g.key, g.label])),
    []
  )

  async function load() {
    try {
      setLoading(true)
      const res = await http.get(`/api/servers/${id}`)
      setData(res)
      setError('')
    } catch (e) {
      setError(e.message || 'Failed to load server')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [id])

  // Logs: poll every 2s only while on the Logs tab
  useEffect(() => {
    if (tab !== 'logs') return
    let cancelled = false
    const tick = async () => {
      try {
        const res = await http.get(`/api/servers/${id}/logs`, { params: { cursor } })
        if (!cancelled && res && Array.isArray(res.lines)) {
          setCursor(res.cursor ?? cursor)
          setLogs(prev => [...prev, ...res.lines])
        }
      } catch { /* ignore for now */ }
    }
    const i = setInterval(tick, 2000)
    return () => { cancelled = true; clearInterval(i) }
  }, [id, tab, cursor])

  // Auto-scroll logs when following
  useEffect(() => {
    if (follow && tab === 'logs' && logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs, follow, tab])

  async function doAction(action) {
    if (busy) return
    const confirmNeeded = action === 'stop' || action === 'restart'
    if (confirmNeeded && !window.confirm(`Are you sure you want to ${action} this server?`)) return

    setBusy(true)
    try {
      // light optimistic feedback
      setData(d => d ? { ...d, status: action === 'stop' ? 'stopping' : 'starting' } : d)
      await http.post(`/api/servers/${id}/${action}`, {})
      await load()
    } catch (e) {
      setError(e.message || `Failed to ${action}`)
    } finally {
      setBusy(false)
    }
  }

  async function sendRcon(e) {
    e.preventDefault()
    const text = cmd.trim()
    if (!text) return
    const ts = new Date().toLocaleTimeString()
    setConsoleLines(prev => [...prev, { ts, kind: 'in', text }])
    setCmd('')

    try {
      const res = await http.post(`/api/servers/${id}/rcon`, { command: text })
      const out = typeof res?.output === 'string' ? res.output : JSON.stringify(res)
      setConsoleLines(prev => [...prev, { ts: new Date().toLocaleTimeString(), kind: 'out', text: out }])
    } catch (e) {
      setConsoleLines(prev => [...prev, { ts: new Date().toLocaleTimeString(), kind: 'out', text: `ERROR: ${e.message}` }])
    }
  }

  async function handleDelete() {
  if (!confirm(`Delete “${server.name}”? This can’t be undone.`)) return;
  await deleteServer(server.id);
  nav("/servers");   // go back to list
}

  if (loading) return <main className="page"><p>Loading…</p></main>
  if (error)   return <main className="page"><p className="login-error">{error}</p></main>
  if (!data)   return <main className="page"><p>Not found.</p></main>

  const gameLabel = gameLabelByKey[data.game] || data.game
  const playersText = (data.players != null && data.maxPlayers != null)
    ? `${data.players}/${data.maxPlayers}` : (data.players ?? '—')

  return (
    <main className="page">
      {/* Header */}
      <div className="dash-header" style={{ marginBottom: 12 }}>
        <div>
          <h1 className="dash-greeting" style={{ marginBottom: 4 }}>{data.name}</h1>
          <div style={{ display:'flex', gap:12, alignItems:'center', flexWrap:'wrap' }}>
            <span><strong>Game:</strong> {gameLabel}</span>
            <span className={`status-pill ${data.status}`}>{data.status}</span>
            <span><strong>Players:</strong> {playersText}</span>
            <span><strong>Uptime:</strong> {formatDuration(data.uptimeSec)}</span>
          </div>
        </div>
        <div style={{ display:'flex', gap:8 }}>
          <button className="btn small" onClick={() => doAction('start')}   disabled={busy || data.status === 'online'}>Start</button>
          <button className="btn small" onClick={() => doAction('stop')}    disabled={busy || data.status === 'offline'}>Stop</button>
          <button className="btn small" onClick={() => doAction('restart')} disabled={busy}>Restart</button>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display:'flex', gap:8, marginBottom:12 }}>
        {['overview','console','logs','settings'].map(t => (
          <button
            key={t}
            className={`btn small ${tab === t ? 'link active' : ''}`}
            onClick={() => setTab(t)}
          >
            {t[0].toUpperCase() + t.slice(1)}
          </button>
        ))}
        <div style={{ marginLeft:'auto' }}>
          <Link to="/servers" className="link">← Back to servers</Link>
        </div>
      </div>

      {/* Panels */}
      {tab === 'overview' && (
        <section className="server-card">
          <h3 style={{ marginTop:0 }}>Overview</h3>
          <div style={{ display:'grid', gap:6, gridTemplateColumns:'repeat(auto-fit, minmax(220px, 1fr))' }}>
            <div><span className="meta-label">Host</span>{data.connection?.host ?? '—'}</div>
            <div><span className="meta-label">Server port</span>{data.connection?.serverPort ?? '—'}</div>
            <div><span className="meta-label">RCON port</span>{data.connection?.rcon?.port ?? '—'}</div>
            <div><span className="meta-label">Query port</span>{data.connection?.queryPort ?? '—'}</div>
          </div>

          {data.paths && (
            <>
              <h4>Paths</h4>
              <div style={{ display:'grid', gap:6 }}>
                <div><span className="meta-label">Root</span>{data.paths.root ?? '—'}</div>
                <div><span className="meta-label">Log</span>{data.paths.log ?? '—'}</div>
              </div>
            </>
          )}

          {data.extras && Object.keys(data.extras).length > 0 && (
            <>
              <h4 style={{ marginTop:12 }}>Game settings</h4>
              <ul>
                {Object.entries(data.extras).map(([k,v]) => (
                  <li key={k}><strong>{k}:</strong> {String(v)}</li>
                ))}
              </ul>
            </>
          )}
        </section>
      )}

      {tab === 'console' && (
        <section className="server-card">
          <h3 style={{ marginTop:0 }}>RCON Console</h3>
          <form onSubmit={sendRcon} style={{ display:'flex', gap:8, marginBottom:12 }}>
            <input
              className="login-input"
              placeholder="Type a command (e.g., say Hello)"
              value={cmd}
              onChange={e => setCmd(e.target.value)}
            />
            <button className="btn small" type="submit">Send</button>
          </form>
          <div style={{
            background:'var(--bg-soft)', border:'1px solid var(--border)', borderRadius:12,
            padding:12, maxHeight:320, overflow:'auto'
          }}>
            {consoleLines.length === 0 ? (
              <div className="muted">No console output yet.</div>
            ) : consoleLines.map((l, i) => (
              <div key={i} style={{ whiteSpace:'pre-wrap', color: l.kind === 'in' ? '#9cc2ff' : 'inherit' }}>
                <span className="muted" style={{ marginRight:6 }}>[{l.ts}]</span>
                {l.kind === 'in' ? `> ${l.text}` : l.text}
              </div>
            ))}
          </div>
        </section>
      )}

      {tab === 'logs' && (
        <section className="server-card">
          <h3 style={{ marginTop:0 }}>Logs</h3>
          <div style={{ display:'flex', alignItems:'center', gap:12, marginBottom:8 }}>
            <label style={{ display:'inline-flex', alignItems:'center', gap:6 }}>
              <input type="checkbox" checked={follow} onChange={e => setFollow(e.target.checked)} />
              Follow
            </label>
            <button className="btn small" onClick={() => { setLogs([]); setCursor(0) }}>Clear</button>
          </div>
          <div style={{
            background:'var(--bg-soft)', border:'1px solid var(--border)', borderRadius:12,
            padding:12, maxHeight:420, overflow:'auto'
          }}>
            {logs.length === 0 ? (
              <div className="muted">Waiting for log lines…</div>
            ) : logs.map((line, i) => <div key={i} style={{ whiteSpace:'pre' }}>{line}</div>)}
            <div ref={logEndRef} />
          </div>
        </section>
      )}

      {tab === 'settings' && (
        <section className="server-card">
          <h3 style={{ marginTop:0 }}>Settings</h3>
          <p>Editing coming later (name, ports, paths, extras, access control).</p>
        </section>
      )}
    </main>
  )
}
