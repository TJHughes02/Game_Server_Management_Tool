import { createContext, useContext, useEffect, useState } from 'react'

const AuthCtx = createContext(null)

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)

    // uses api/me
    useEffect(() => {
        const raw = localStorage.getItem('authUser')
        if (raw) setUser(JSON.parse(raw))
    }, [])

    // helper to log out everywhere (not impl yet)
    function logout() {
        localStorage.removeItem('authUser')
        setUser(null)
    }

    return (
        <AuthCtx.Provider value={{ user, setUser, logout }}>
            {children}
        </AuthCtx.Provider>
    )
}

export function useAuth() {
    return useContext(AuthCtx)
}
