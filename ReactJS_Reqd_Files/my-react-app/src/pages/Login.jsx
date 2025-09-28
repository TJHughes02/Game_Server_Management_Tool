import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx' 
// should no longer use 'demouser' that I had set previously

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

  return (
    <main className="page center gray-bg">
      <form className="card form" onSubmit={handleSubmit}>
        <h2 className="title">Log in</h2>
        {backendStatus === 'ok' && <div className="muted small">Backend: OK</div>}
        {backendStatus === 'down' && <div className="error">Backend not reachable</div>}

        <label className="label">
          Display name
          <input className="input" value={displayName}
                 onChange={e => setDisplayName(e.target.value)} autoFocus />
        </label>

        <label className="label">
          Password
          <input className="input" type="password" value={password}
                 onChange={e => setPassword(e.target.value)} />
        </label>

        {error && <div className="error">{error}</div>}
        <button className="btn primary full" disabled={!canSubmit || loading}>
          {loading ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </main>
  )
}
