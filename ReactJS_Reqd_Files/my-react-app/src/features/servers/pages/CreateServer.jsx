import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { GAMES, GAME_DEFAULTS, GAME_EXTRAS } from '@/constants/games.js'
import { http } from '@/services/http.js'

/** Base fields required for ANY server */
const BASE_FIELDS = [
    { name: 'name', label: 'Server name', type: 'text', required: true },
    { name: 'game', label: 'Game', type: 'select', required: true },
    { name: 'host', label: 'Host/IP', type: 'text', required: true, placeholder: 'localhost or IP' },
    { name: 'serverPort', label: 'Server port', type: 'number', required: true },
    { name: 'rconPort', label: 'RCON port', type: 'number', required: true },
    { name: 'rconPass', label: 'RCON password', type: 'password', required: true },
    { name: 'queryPort', label: 'Query port', type: 'number', required: false, placeholder: 'optional' },
]

export default function CreateServer() {
    const nav = useNavigate()

    // initialize with first game’s defaults (if present)
    const defaultGame = GAMES[0]?.key ?? 'minecraft'
    const d = GAME_DEFAULTS[defaultGame] || {}

    const [form, setForm] = useState({
        name: '',
        game: defaultGame,
        host: 'localhost',
        serverPort: d.serverPort ?? '',
        rconPort: d.rconPort ?? '',
        rconPass: '',
        queryPort: d.queryPort ?? '',
    })
    const [touched, setTouched] = useState({})
    const [submitting, setSubmitting] = useState(false)
    const [submitError, setSubmitError] = useState('')

    // extras for current game come from constants
    const extras = GAME_EXTRAS[form.game] || []
    const schema = useMemo(() => [...BASE_FIELDS, ...extras], [form.game, extras.length])

    // when game changes, prefill sensible defaults for ports
    function handleGameChange(nextGame) {
        const nd = GAME_DEFAULTS[nextGame] || {}
        setForm(prev => ({
            ...prev,
            game: nextGame,
            serverPort: prev.serverPort || nd.serverPort || '',
            rconPort: prev.rconPort || nd.rconPort || '',
            queryPort: prev.queryPort || nd.queryPort || '',
        }))
    }

    function setField(name, value) { setForm(prev => ({ ...prev, [name]: value })) }
    function markTouched(name) { setTouched(prev => ({ ...prev, [name]: true })) }

    // simple required validation
    const errors = {}
    schema.forEach(f => {
        if (f.required && !String(form[f.name] ?? '').trim()) errors[f.name] = 'Required'
    })
    const hasErrors = Object.keys(errors).length > 0

    async function handleSubmit(e) {
        e.preventDefault()

        // mark all touched so inline errors show
        const allTouched = {}
        schema.forEach(f => { allTouched[f.name] = true })
        setTouched(allTouched)
        setSubmitError('')
        if (hasErrors) return

        // flat payload (matches models)
        const payload = {
            name: form.name,
            game_type: form.game,
            server_port: Number(form.serverPort),

            // RCON / paths 
            rcon_host: form.host.trim(),
            rcon_port: Number(form.rconPort),
            rcon_pass_hash: form.rconPass,

            install_path: "", // fully in backend
            server_host_name: form.host.trim(),
            rcon_user: "admin",                      // dev default
            java_path: "C:\\Program Files\\Java\\bin\\java.exe",  // dev default
            steam_cmd_path: "C:\\steamcmd\\steamcmd.exe"          // dev default
        }

        try {
            setSubmitting(true)

            // send only ONE request to your canonical route
            //    (use '/api/servers' if you added that; otherwise switch this to '/api/servers/new')
            await http.post('/api/servers', payload)

            nav('/servers')
        } catch (err) {
            // show useful details from the backend
            const msg =
                (err.body && (err.body.error || err.body.message)) ||
                err.message || 'Failed to create server'
            setSubmitError(`${msg}${err.status ? ` (HTTP ${err.status})` : ''}`)
        } finally {
            setSubmitting(false)
        }
    }


    return (
        <main className="page">
            <h1>Create Server</h1>

            <form onSubmit={handleSubmit} noValidate>
                {schema.map(field => {
                    const val = form[field.name] ?? ''
                    const err = touched[field.name] && field.required && !String(val).trim()

                    return (
                        <div key={field.name} style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', marginBottom: 4 }}>
                                {field.label}{field.required ? ' *' : ''}
                            </label>

                            {field.type === 'select' ? (
                                <select
                                    value={form.game}
                                    onChange={e => handleGameChange(e.target.value)}
                                    onBlur={() => markTouched('game')}
                                >
                                    {GAMES.map(g => (
                                        <option key={g.key} value={g.key}>{g.label}</option>
                                    ))}
                                </select>
                            ) : (
                                <input
                                    type={field.type}
                                    value={val}
                                    placeholder={field.placeholder || ''}
                                    onChange={e => setField(field.name, e.target.value)}
                                    onBlur={() => markTouched(field.name)}
                                    aria-invalid={err ? 'true' : 'false'}
                                />
                            )}

                            {field.help && <div style={{ fontSize: 12, color: '#a0a6b1' }}>{field.help}</div>}
                            {err && <div style={{ fontSize: 12, color: '#ff9aa6' }}>This field is required.</div>}
                        </div>
                    )
                })}

                {submitError && (
                    <div className="login-error" style={{ marginBottom: 12 }}>{submitError}</div>
                )}

                <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
                    <button type="submit" disabled={submitting}>
                        {submitting ? 'Creating…' : 'Create server'}
                    </button>
                    <button type="button" onClick={() => nav(-1)} disabled={submitting}>Cancel</button>
                </div>

                <details style={{ marginTop: 16 }}>
                    <summary>Preview payload</summary>
                    <pre>{JSON.stringify({
                        name: form.name,
                        game: form.game,
                        connection: {
                            host: form.host,
                            serverPort: form.serverPort,
                            rcon: { port: form.rconPort, password: form.rconPass },
                            queryPort: form.queryPort,
                        },
                        extras: (GAME_EXTRAS[form.game] || []).reduce((acc, f) => { acc[f.name] = form[f.name] ?? ''; return acc }, {}),
                    }, null, 2)}</pre>
                </details>
            </form>
        </main>
    )
}
