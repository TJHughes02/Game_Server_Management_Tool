import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'
import { GAMES } from '@/constants/games.js'

export default function Dashboard() {
  const { user } = useAuth()
  const nav = useNavigate()


  // THIS ENTIRE SECTION BELOW IS TEMPORARTY AND ONLY A TEMPLATE. MOST OF THIS WILL NOT BE USED
  // IN THE FINAL PRODUCT.


  // Template servers (placeholder until your create-server flow exists)
  const servers = [
    { id: 1, name: 'Survival SMP', game: 'Minecraft', status: 'online', players: '3/20', uptime: '2h 14m' },
    { id: 2, name: 'PvP Arena', game: 'Rust', status: 'offline', players: '0/50', uptime: '—' },
    { id: 3, name: 'Island Base', game: 'ARK', status: 'starting', players: '—', uptime: '—' },
    { id: 4, name: 'Modded SMP', game: 'Minecraft', status: 'offline', players: '0/10', uptime: '—' },
    { id: 5, name: 'Modded SMP', game: 'Minecraft', status: 'offline', players: '0/10', uptime: '—' },
    { id: 6, name: 'Modded SMP', game: 'Minecraft', status: 'offline', players: '0/10', uptime: '—' },
    { id: 7, name: 'Modded SMP', game: 'Minecraft', status: 'starting', players: '0/10', uptime: '—' },
    { id: 8, name: 'Modded SMP', game: 'Minecraft', status: 'online', players: '0/10', uptime: '—' },
    { id: 9, name: 'Survival SMP', game: 'Minecraft', status: 'online', players: '3/20', uptime: '2h 14m' },
    { id: 10, name: 'PvP Arena', game: 'Rust', status: 'offline', players: '0/50', uptime: '—' },
    { id: 11, name: 'Island Base', game: 'ARK', status: 'starting', players: '—', uptime: '—' },
    { id: 12, name: 'Modded SMP', game: 'Minecraft', status: 'offline', players: '0/10', uptime: '—' },
    { id: 13, name: 'Modded SMP', game: 'Minecraft', status: 'offline', players: '0/10', uptime: '—' },
    { id: 14, name: 'Modded SMP', game: 'Minecraft', status: 'offline', players: '0/10', uptime: '—' },
    { id: 15, name: 'Modded SMP', game: 'Minecraft', status: 'starting', players: '0/10', uptime: '—' },
    { id: 16, name: 'Modded SMP', game: 'Minecraft', status: 'online', players: '0/10', uptime: '—' },
  ]

  return (
    <main className="page">
      <div className="dash">
        {/* Left 1/3 — compatible games (driven by constants/games.js) */}
        <aside className="dash-sidebar">
          <h2 className="dash-title">Compatible games</h2>
          <p className="muted">Examples (RCON):</p>
          <ul className="games-list">
            {GAMES.slice(0, 7).map(g => ( // (leave this number, increase/decrease for list size)
              <li key={g.key}>{g.label}</li>
            ))}
          </ul>

          <Link to="/games" className="btn view-all">View all compatible games</Link>
        </aside>

        {/* Right 2/3 — servers */}
        <section className="dash-main">
          <header className="dash-header">
            <div>
              <h1 className="dash-greeting">Dashboard</h1>
              <p className="muted">Welcome{user?.display_name ? `, ${user.display_name}` : ''}!</p>
            </div>
            <button
              className="btn primary"
              onClick={() => nav('/servers/new')}
              title="Create a new server"
            >
              + Create server
            </button>
          </header>

          <div className="servers-grid">
            {servers.map(s => (
              <article key={s.id} className={`server-card ${s.status}`}>
                <div className="server-top">
                  <h3 className="server-name">{s.name}</h3>
                  <span className={`status-pill ${s.status}`}>{s.status}</span>
                </div>
                <div className="server-meta">
                  <div><span className="meta-label">Game</span>{s.game}</div>
                  <div><span className="meta-label">Players</span>{s.players}</div>
                  <div><span className="meta-label">Uptime</span>{s.uptime}</div>
                </div>
                <div className="server-actions">
                  <Link to={`/servers/${s.id}`} className="btn small">Open</Link>
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}