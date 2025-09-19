import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login() {
const [email, setEmail] = useState('')
const [password, setPassword] = useState('')
const [loading, setLoading] = useState(false)
const [error, setError] = useState('')
const nav = useNavigate()

// Must be longer than 3 chars (definitely subject to change)
const canSubmit = email.length > 3 && password.length > 3


async function handleSubmit(e) {
e.preventDefault()
setError('')
setLoading(true)

// For now, accept any non-trivial credentials
const fakeUser = { id: 'demo', email }
localStorage.setItem('demoUser', JSON.stringify(fakeUser))
setLoading(false)
nav('/dashboard')
}

function loginAsDemo() {
    const fakeUser = { id: 'demo', email: 'demo@server.local' }
    localStorage.setItem('demoUser', JSON.stringify(fakeUser))
    nav('/dashboard')
}

// formatting
return (
    <main className="page center gray-bg">
        <form className="card form" onSubmit={handleSubmit}>
            <h2 className="title">Log in</h2>
            <label className="label">
                Email
                <input
                    className="input"
                    type="email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    placeholder="you@example.com"
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
            <button type="button" className="btn full" onClick={loginAsDemo}>
                Continue as Demo
            </button>
            <p className="muted small center-text">
                This is a mock login. No credentials are sent anywhere.
            </p>
        </form>
    </main>
)
}

/*
 * THIS IS A DEMO PAGE. MOST OF THIS WILL HAVE TO BE REPLACED. THIS IS JUST TESTING
    THAT I REMEMBER HOW TO DO REACT METHODS AND OTHER MISC FUNCTIONS.

    DO NOT USE FOR FINAL PROJECT - DO NOT USE FOR FINAL PROJECT - DO NOT USE FOR FINAL PROJECT
 */