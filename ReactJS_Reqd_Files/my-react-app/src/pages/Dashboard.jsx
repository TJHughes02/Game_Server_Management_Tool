import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'


export default function Dashboard() {
    const [user, setUser] = useState(null)
    const nav = useNavigate()
    useEffect(() => {
        const raw = localStorage.getItem('demoUser')
        if (raw) setUser(JSON.parse(raw))
    }, [])


    function logout() {
        localStorage.removeItem('demoUser')
        nav('/login')
    }


    return (
        <main className="page">
            <div className="container">
                <h1>Dashboard</h1>
                <p className="muted">Welcome{user?.email ? `, ${user.email}` : ''}!</p>
                <div className="grid">
                    <div className="tile">
                        <h3>Servers</h3>
                        <p className="muted">No servers yet. Add one later.</p>
                    </div>
                    <div className="tile">
                        <h3>Backups</h3>
                        <p className="muted">Set up rolling backups per node. (temporary)</p>
                    </div>
                    <div className="tile">
                        <h3>Console</h3>
                        <p className="muted">Live log & RCON coming soon.(cant promise but maybe)</p>
                    </div>
                </div>
                <button className="btn" onClick={logout}>Log out</button>
            </div>
        </main>
    )
}