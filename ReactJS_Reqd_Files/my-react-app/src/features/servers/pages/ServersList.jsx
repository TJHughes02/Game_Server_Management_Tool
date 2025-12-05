// src/features/servers/pages/ServersList.jsx
import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { http } from '@/services/http.js'
import { GAMES } from '@/constants/games.js'
//import { useUptime } from '../../hooks/useUptime.js'


export default function ServersList() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const gameLabelByKey = useMemo(
    () => Object.fromEntries(GAMES.map(g => [g.key, g.label])),
    []
  )

  useEffect(() => {
    (async () => {
      try {
        const data = await http.get('/api/servers')
        setItems(Array.isArray(data) ? data : [])
      } catch (e) {
        setError(e.message || 'Failed to load servers')
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  if (loading) return <main className="page"><p>Loading servers…</p></main>
  if (error)   return <main className="page"><p className="login-error">{error}</p></main>

  return (
    <main className="page">
      <header className="dash-header" style={{ marginBottom: 16 }}>
        <div>
          <h1 className="dash-greeting">Servers</h1>
          <p className="muted">Manage all game servers from one place.</p>
        </div>
        <Link to="/servers/new" className="btn small">+ Create server</Link>
      </header>

      {items.length === 0 ? (
        <p>No servers yet. <Link to="/servers/new">Create your first server</Link>.</p>
      ) : (
        <div className="servers-grid">
          {items.map(s => {
            const upTimeSec = s.started_at ? useUptime(s.started_at) : 0
            const gameLabel = gameLabelByKey[s.game] || s.game
            const playersText =
              s.players != null && s.maxPlayers != null ? `${s.players}/${s.maxPlayers}` :
              s.players != null ? String(s.players) : '—'

            return (
              <article key={s.id} className={`server-card ${s.status}`}>
                <div className="server-top">
                  <h3 className="server-name">{s.name}</h3>
                  <span className={`status-pill ${s.status}`}>{s.status}</span>
                </div>

                <div className="server-meta">
                  <div><span className="meta-label">Game</span>{gameLabel}</div>
                  <div><span className="meta-label">Players</span>{playersText}</div>
                  <div><span className="meta-label">Uptime</span>{formatDuration(upTimeSec)}</div>
                </div>

                <div className="server-actions">
                  <Link to={`/servers/${s.id}`} className="btn small">Open</Link>
                </div>
              </article>
            )
          })}
        </div>
      )}
    </main>
  )
}


// currently does not work, will work if curled