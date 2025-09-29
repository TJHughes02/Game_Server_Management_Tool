import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx' 

export default function Login() {
  const [displayName, setDisplayName] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [backendStatus, setBackendStatus] = useState(null)
  const nav = useNavigate()
  const { setUser } = useAuth()

  useEffect(() => {
    fetch('/api/health')
      .then(r => (r.ok ? r.json() : Promise.reject()))
      .then(() => setBackendStatus('ok'))
      .catch(() => setBackendStatus('down'))
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ display_name: displayName, password })
      })
      const data = await res.json().catch(() => ({}))

      if (!res.ok) throw new Error(data.Status || 'Login failed')

      // Expecting backend to return { Status: "...", user: { id, display_name, ... } }
      if (!data.user) throw new Error('No user returned from server')

      localStorage.setItem('authUser', JSON.stringify(data.user))
      setUser(data.user)
      nav('/dashboard')
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const canSubmit = displayName.trim() && password

  // for the username section, we might only use 'username' instead of email, unsure about this for now.
   return (
    <main className="page login-hero">
      <div className="login-card">
        <div className="login-header">
          <div className="login-badge">Game Server Management Tool</div>
          <h2 className="login-title">Welcome back</h2>
          <p className="login-subtitle">Sign in to access your dashboard</p>
          {backendStatus === 'ok' && <div className="login-status ok">Backend: OK</div>}
          {backendStatus === 'down' && <div className="login-status bad">Backend not reachable</div>}
        </div>
        <form className="login-form" onSubmit={handleSubmit}>
          <label className="login-label">
            <span>Username</span> 
            <input
              className="login-input"
              value={displayName}
              onChange={e => setDisplayName(e.target.value)}
              placeholder=""
              autoFocus
            />
          </label>

          <label className="login-label">
            <span>Password</span>
            <input
              className="login-input"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder=""
            />
          </label>

          {error && <div className="login-error">{error}</div>}

          <button className="login-button" disabled={!canSubmit || loading}>
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <div className="login-footer">
          <span className="login-hint">Need an account? Ask your admin.</span>
        </div>
      </div>

      <div className="login-accent" aria-hidden="true" />
    </main>
  )
}
