import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'
import { http } from '@/services/http'

export default function Login() {
  const [displayName, setDisplayName] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [backendStatus, setBackendStatus] = useState(null)
  const [touched, setTouched] = useState({ displayName: false, password: false })
  const [triedSubmit, setTriedSubmit] = useState(false)
  const nav = useNavigate()
  const { setUser } = useAuth()

  useEffect(() => {
    //fetch('/api/health')
    http.get('/api/health')
      .then(r => (r.ok ? r.json() : Promise.reject()))
     .then(() => setBackendStatus('ok'))
      .catch(() => setBackendStatus('down'))
  }, [])

  // displayname && password
  const dnEmpty = displayName.trim().length === 0
  const pwEmpty = password.length === 0
  const showDnError = (touched.displayName || triedSubmit) && dnEmpty
  const showPwError = (touched.password || triedSubmit) && pwEmpty
  const canSubmit = !dnEmpty && !pwEmpty

  function markTouched(field) {
    setTouched(prev => ({ ...prev, [field]: true }))
  }


  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setTriedSubmit(true)

    if (!canSubmit) {
      // Don’t send; highlight fields and show messages
      return
    }

    setLoading(true)
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ display_name: displayName, password })
      })
      //const data = await res.json().catch(() => ({}))

      //if (!res.ok) throw new Error(data.Status || 'Login failed')
      //if (!data.user) throw new Error('No user returned from server')
      const data = await http.post('/api/login', {
        display_name: displayName, password
      })
      if (!data?.user) throw new Error('No user returned from server')

      localStorage.setItem('authUser', JSON.stringify(data.user))
      setUser(data.user)
      nav('/dashboard')
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  //const canSubmit = displayName.trim() && password

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

        {/* Global API error (e.g., wrong password) */}
        {error && <div className="login-error" role="alert">{error}</div>}

        <form className="login-form" onSubmit={handleSubmit} noValidate>
          <label className="login-label">
            <span>Display name</span>
            <input
              className={`login-input${showDnError ? ' invalid' : ''}`}
              value={displayName}
              onChange={e => setDisplayName(e.target.value)}
              onBlur={() => markTouched('displayName')}
              placeholder=""
              aria-invalid={showDnError ? 'true' : 'false'}
              aria-describedby="displayNameError"
              autoFocus
            />
            {showDnError && (
              <div id="displayNameError" className="field-error">Must enter username</div>
            )}
          </label>

          <label className="login-label">
            <span>Password</span>
            <input
              className={`login-input${showPwError ? ' invalid' : ''}`}
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              onBlur={() => markTouched('password')}
              placeholder=""
              aria-invalid={showPwError ? 'true' : 'false'}
              aria-describedby="passwordError"
            />
            {showPwError && (
              <div id="passwordError" className="field-error">Must enter password</div>
            )}
          </label>

          <button className="login-button" disabled={loading}>
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
