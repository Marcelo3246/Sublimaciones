import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { EVENTO_SESION_EXPIRADA, loadSession } from '../../api/sesion.js'
import { logout } from './api.js'

const SesionContext = createContext(null)

// Las sesiones simuladas guardadas antes de existir los permisos no traían
// esGlobal; el usuario de prueba es administrador.
function sesionInicial() {
  const guardada = loadSession()
  if (guardada?.access === 'mock-access' && guardada.usuario && guardada.usuario.esGlobal === undefined) {
    return { ...guardada, usuario: { id: 1, local: 1, ...guardada.usuario, esGlobal: true } }
  }
  return guardada
}

/** Guarda la sesión iniciada y la comparte con todas las páginas. */
export function SesionProvider({ children }) {
  const [sesion, setSesion] = useState(sesionInicial)

  const cerrarSesion = useCallback(() => {
    logout()
    setSesion(null)
  }, [])

  // Si el backend rechaza el token (api/cliente.js), se vuelve al login.
  useEffect(() => {
    const alExpirar = () => setSesion(null)
    window.addEventListener(EVENTO_SESION_EXPIRADA, alExpirar)
    return () => window.removeEventListener(EVENTO_SESION_EXPIRADA, alExpirar)
  }, [])

  const valor = useMemo(() => ({ sesion, iniciarSesion: setSesion, cerrarSesion }), [sesion, cerrarSesion])

  return <SesionContext.Provider value={valor}>{children}</SesionContext.Provider>
}

export function useSesion() {
  return useContext(SesionContext)
}

/**
 * Envuelve las páginas que necesitan sesión; si no hay, manda al login.
 * Con `soloAdmin`, los usuarios sin acceso global vuelven al dashboard.
 */
export function RutaProtegida({ soloAdmin = false, children }) {
  const { sesion } = useSesion()
  const location = useLocation()

  if (!sesion) {
    // Se recuerda la página pedida para volver a ella después de ingresar.
    return <Navigate to="/login" replace state={{ desde: location.pathname }} />
  }
  if (soloAdmin && !sesion.usuario?.esGlobal) return <Navigate to="/" replace />
  return children
}
