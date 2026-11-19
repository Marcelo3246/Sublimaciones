import Login from './Login.jsx'

// Ruta pública: la única que se ve sin sesión.
export const rutas = [{ path: '/login', element: <Login />, publica: true }]
