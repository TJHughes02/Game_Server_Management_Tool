import { Link, NavLink } from 'react-router-dom'


export default function NavBar() {
    return (
        <nav className="navbar">
            <div className="nav-inner">
                <Link to="/" className="brand">Game Server Management Tool</Link>
                <div className="nav-links">
                    <NavLink to="/" end className={({ isActive }) => isActive ? 'link active' : 'link'}>Home</NavLink>
                    <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'link active' : 'link'}>Dashboard</NavLink>
                    <NavLink to="/login" className={({ isActive }) => isActive ? 'btn small primary' : 'btn small'}>Log in</NavLink>
                </div>
            </div>
        </nav>
    )
}