import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext.jsx'
import { http } from '@/services/http.js'
import { GAMES } from '@/constants/games.js'

export default function Dashboard() {
  const { user } = useAuth()
  const nav = useNavigate()
  const [servers, setServers] = useState([])
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
        setServers(Array.isArray(data) ? data : [])
      } catch (e) {
        setError(e.message || 'Failed to load servers')
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  return (
    <main className="page">
      <div className="dash">
        <aside className="dash-sidebar">
          <h2 className="dash-title">Compatible games</h2>
          <p className="muted">Examples (RCON):</p>
          <ul className="games-list">
            {GAMES.slice(0, 4).map(g => <li key={g.key}>{g.label}</li>)}
          </ul>
          <Link to="/games" className="btn view-all">View all compatible games</Link>
        </aside>

        <section className="dash-main">
          <header className="dash-header">
            <div>
              <h1 className="dash-greeting">Dashboard</h1>
              <p className="muted">Welcome{user?.display_name ? `, ${user.display_name}` : ''}!</p>
            </div>
            <button className="btn primary" onClick={() => nav('/servers/new')}>
              + Create server
            </button>
          </header>

          {loading ? (
            <p>Loading servers…</p>
          ) : error ? (
            <p className="login-error">{error}</p>
          ) : servers.length === 0 ? (
            <p>No servers yet. <Link to="/servers/new">Create your first server</Link>.</p>
          ) : (
            <div className="servers-grid">
              {servers.map(s => (
                <article key={s.id} className={`server-card ${s.status}`}>
                  <div className="server-top">
                    <h3 className="server-name">{s.name}</h3>
                    <span className={`status-pill ${s.status}`}>{s.status}</span>
                  </div>
                  <div className="server-meta">
                    <div><span className="meta-label">Game</span>{gameLabelByKey[s.game] || s.game}</div>
                    <div><span className="meta-label">Players</span>{s.players ?? '—'}</div>
                    <div><span className="meta-label">Uptime</span>{(s.uptimeSec ?? 0) > 0 ? `${Math.floor(s.uptimeSec/60)}m` : '—'}</div>
                  </div>
                  <div className="server-actions">
                    <Link to={`/servers/${s.id}`} className="btn small">Open</Link>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  )
}
