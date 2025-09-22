import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [displayName, setDisplayName] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [backendStatus, setBackendStatus] = useState(null)
  const nav = useNavigate()

 // api ping
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
        body: JSON.stringify({
          display_name: displayName,
          password: password,
        }),
      })

      const data = await res.json().catch(() => ({}))

      if (!res.ok) {
        // Flask returns 401 with a status message on bad entry
        throw new Error(data.Status || 'Login failed')
      }

      // Success (HTTP 200). backend returns a Status string only
      // HAVE NOT DONE USER TOKENS YET
      nav('/dashboard')
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const canSubmit = displayName.trim().length > 0 && password.length > 0

  return (
    <main className="page center gray-bg">
      <form className="card form" onSubmit={handleSubmit}>
        <h2 className="title">Log in</h2>

        {backendStatus === 'ok' && (
          <div className="muted small">Backend: OK</div>
        )}
        {backendStatus === 'down' && (
          <div className="error">Backend not reachable</div>
        )}

        <label className="label">
          Display name
          <input
            className="input"
            type="text"
            value={displayName}
            onChange={e => setDisplayName(e.target.value)}
            placeholder="e.g., TestUser"
            autoFocus
          />
        </label>

        <label className="label">
          Password
          <input
            className="input"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="••••••••"
          />
        </label>

        {error && <div className="error">{error}</div>}

        <button className="btn primary full" disabled={!canSubmit || loading}>
          {loading ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </main>
  )
}
