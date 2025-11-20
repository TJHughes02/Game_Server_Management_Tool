import { Routes, Route, Navigate } from 'react-router-dom'
//import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Games from './pages/Games.jsx'
//import CreateServer from "./features/servers/pages/CreateServer.jsx"
import NavBar from './components/NavBar.jsx'
import { AuthProvider, useAuth } from './context/AuthContext.jsx'


import CreateServer from './features/servers/pages/CreateServer.jsx'
import ServersList from './features/servers/pages/ServersList.jsx'
import ServerDetail from './features/servers/pages/ServerDetail.jsx'


//function ProtectedRoute({ children }) {
  //const { user } = useAuth()
  //return user ? children : <Navigate to="/login" replace />
//}

function ProtectedRoute({ children }) {
  const { user, booting } = useAuth();
  if (booting) return null;
  return user ? children : <Navigate to="/login" replace />;
}


// top portion is unprotected (not locked behind login) <Route>
// bottom portion is protected (locked behind login) <ProtectedRoute>
export default function App() {
  return (
    <AuthProvider>
      <div className="app-shell">
        <NavBar />
        <Routes>
          {/* Public */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/games" element={<Games />} />

          {/* Protected */}
          <Route
            path="/dashboard"
            element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
          />
          <Route
            path="/servers/new"
            element={<ProtectedRoute><CreateServer /></ProtectedRoute>}
          />
          <Route
            path="/servers/:id"
            element={<ProtectedRoute><ServerDetail /></ProtectedRoute>}
          />

          {/* Returns 404 */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </AuthProvider>
  )
}
