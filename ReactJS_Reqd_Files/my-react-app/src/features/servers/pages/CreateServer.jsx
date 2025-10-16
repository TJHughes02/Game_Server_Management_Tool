import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'


/**
 * RCON-friendly games you plan to support (extend anytime).
 * key = stable id you’ll also use on the backend
 */
const GAMES = [
    { key: 'minecraft', label: 'Minecraft (Java Edition)' },
    { key: 'rust', label: 'Rust' },
    { key: 'ark', label: 'ARK: Survival Evolved' },
    { key: 'csgo', label: 'Counter-Strike: Global Offensive' },
    { key: 'factorio', label: 'Factorio' },
]
// THIS PART ABOVE WILL BE CHANGED TO BE ABLE TO BE CHANGED IN 1 FILE AND
// SYNC BETWEEN MULTIPLE e.g. list.jsx will include the games and games and this file
// will be able to display the games depending on what is in list.

/**
 * Game defaults + extra fields.
 * Each field object: { name, label, type, required?, placeholder?, help? }
 * Keep baseFields small and generic; add per-game extras as needed.
 */
const GAME_CONFIG = {
    // defaults for shared fields per game (server & rcon ports differ by title)
    defaults: {
        minecraft: { serverPort: 25565, rconPort: 25575 },
        rust: { serverPort: 28015, rconPort: 28016 },
        ark: { serverPort: 7777, rconPort: 27020, queryPort: 27015 },
        csgo: { serverPort: 27015, rconPort: 27015 },
        factorio: { serverPort: 34197, rconPort: 27015 },
    },
    // extra per-game fields (optional but want to put in)
    extras: {
        // will add soon
    },
}

/** Base fields required for ANY server */
const BASE_FIELDS = [
    { name: 'name', label: 'Server name', type: 'text', required: true },
    { name: 'game', label: 'Game', type: 'select', required: true },
    { name: 'host', label: 'Host/IP', type: 'text', required: true, placeholder: 'localhost or IP' },
    { name: 'serverPort', label: 'Server port', type: 'number', required: true },
    { name: 'rconPort', label: 'RCON port', type: 'number', required: true },
    { name: 'rconPass', label: 'RCON password', type: 'password', required: true },
    // Optional but common on Source/Steam titles:
    { name: 'queryPort', label: 'Query port', type: 'number', required: false, placeholder: 'optional' },
]

export default function CreateServer() {
    const nav = useNavigate()

    // initial form state
    const [form, setForm] = useState({
        name: '',
        game: GAMES[0].key, // default to first game
        host: 'localhost',
        serverPort: '',
        rconPort: '',
        rconPass: '',
        queryPort: '',
    })
    const [touched, setTouched] = useState({})

    // derive schema: base + extras for selected game
    const extras = GAME_CONFIG.extras[form.game] || []
    const schema = useMemo(() => [...BASE_FIELDS, ...extras], [form.game])

    // when game changes, prefill sensible defaults for ports (without clobbering typed values)
    function handleGameChange(nextGame) {
        const d = GAME_CONFIG.defaults[nextGame] || {}
        setForm(prev => ({
            ...prev,
            game: nextGame,
            serverPort: prev.serverPort || d.serverPort || '',
            rconPort: prev.rconPort || d.rconPort || '',
            queryPort: prev.queryPort || d.queryPort || '',
        }))
    }

    function setField(name, value) {
        setForm(prev => ({ ...prev, [name]: value }))
    }
    function markTouched(name) {
        setTouched(prev => ({ ...prev, [name]: true }))
    }

    // simple required validation
    const errors = {}
    schema.forEach(f => {
        if (f.required && !String(form[f.name] ?? '').trim()) {
            errors[f.name] = 'Required'
        }
    })
    const hasErrors = Object.keys(errors).length > 0

    async function handleSubmit(e) {
        e.preventDefault()
        // mark everything as touched so errors show
        const allTouched = {}
        schema.forEach(f => { allTouched[f.name] = true })
        setTouched(allTouched)

        if (hasErrors) return

        // Build a payload that’s easy to extend on the backend later.
        const payload = {
            name: form.name,
            game: form.game,
            connection: {
                host: form.host,
                serverPort: Number(form.serverPort),
                rcon: {
                    port: Number(form.rconPort),
                    password: form.rconPass,
                },
                queryPort: form.queryPort ? Number(form.queryPort) : undefined,
            },
            // 
        }

        // TODO: later  POST to your Flask endpoint

        // For now, just navigate back to dashboard and pass state or show a toast
        console.log('Create server payload:', payload)
        nav('/dashboard')
    }
    // payload = formatting for server data going into table
    return (
        <main className="page">
            <h1>Create Server</h1>

            <form onSubmit={handleSubmit} noValidate>
                {/* Base + dynamic fields */}
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
                                    {GAMES.map(g => <option key={g.key} value={g.key}>{g.label}</option>)}
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

                {/* Actions */}
                <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
                    <button type="submit">Create server</button>
                    <button type="button" onClick={() => nav(-1)}>Cancel</button>
                </div>

                {/* (Optional) quick debug preview so you can see what will be sent */}
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
                        extras: (GAME_CONFIG.extras[form.game] || []).reduce((acc, f) => { acc[f.name] = form[f.name] ?? ''; return acc }, {}),
                    }, null, 2)}</pre>
                </details>
            </form>
        </main>
    )
}
