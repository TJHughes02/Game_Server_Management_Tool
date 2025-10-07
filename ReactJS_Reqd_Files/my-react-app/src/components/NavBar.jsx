import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../context/AuthContext.jsx'

export default function NavBar() {
  const { user, logout } = useAuth()
  const [busy, setBusy] = useState(false)
  const nav = useNavigate()

  async function handleLogout() {
    if (busy) return
    setBusy(true)
    try {
      await logout()                 // calls /api/logout with credentials
      nav('/login', { replace: true })
    } finally {
      setBusy(false)
    }
  }

  return (
    <header className="navbar">
      <div className="nav-inner">
        <Link to="/" className="brand">Game Server Management Tool</Link>

        <nav className="nav-links">
          <NavLink to="/" className="link">Home</NavLink>
          <NavLink to="/games" className="link">Games</NavLink>
          {user && <NavLink to="/dashboard" className="link">Dashboard</NavLink>}

          {!user ? (
            <Link to="/login" className="btn small">Log in</Link>
          ) : (
            <button
              className="btn small"
              onClick={handleLogout}
              disabled={busy}
              title={`Signed in as ${user.display_name}`}
            >
              {busy ? 'Logging out…' : 'Log out'}
            </button>
          )}
        </nav>
      </div>
    </header>
  )
}
