import { Link } from 'react-router-dom'


export default function Home() {
    return (
        <main className="page center gray-bg">
            <div className="card">
                <h1 className="title">Server Manager</h1>
                <p className="muted">
                    Manage your game servers from a single dashboard. Start/stop servers,
                    view players, schedule backups, and more. (Might be too much, will check later)
                </p>
                <div className="row gap">
                    <Link className="btn primary" to="/login">Log in</Link>
                    <a className="btn" href="#features">Learn more</a>
                </div>
            </div>


            <section id="features" className="features">
                <div className="feature">
                    <h3>Backups</h3>
                    <p>Filler</p>
                </div>
                <div className="feature">
                    <h3>Console</h3>
                    <p>Filler (is this possible?)</p>
                </div>
                <div className="feature">
                    <h3>Multi-node</h3>
                    <p>Switch between nodes and manage per-node permissions. (Should be good)</p>
                </div>
            </section>
        </main>
    )
}