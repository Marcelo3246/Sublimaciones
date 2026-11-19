/**
 * Cliente de autenticación contra el backend Django (SimpleJWT).
 *
 * Rutas del PR #3 del repo oficial (backend/config/urls.py y backend/apps/core/urls.py),
 * definidas en RUTAS_AUTH de src/api/config.js:
 *   POST {VITE_API_URL}/auth/token/          { nombre_usuario, password } -> { access, refresh }
 *   POST {VITE_API_URL}/auth/token/refresh/  { refresh } -> { access, refresh }
 *   GET  {VITE_API_URL}/core/perfil/         -> UsuarioSerializer de request.user
 *
 * El backend todavía no tiene ruta de logout (no instala token_blacklist): cerrar
 * sesión solo borra los tokens del navegador.
 *
 * Mientras el backend no esté disponible, VITE_AUTH_MOCK=true simula el login
 * en el navegador con el usuario de prueba DEMO_USER.
 */

import { API_URL, RUTAS_AUTH } from '../../api/config.js'
import { clearSession, loadSession, saveSession } from '../../api/sesion.js'
import { anotarAccion } from '../../api/mock/bitacora.js'

const USE_MOCK = import.meta.env.VITE_AUTH_MOCK === 'true'

export const DEMO_USER = {
  usuario: 'admin',
  correo: 'admin@sublimacion.com',
  password: 'admin123',
  nombre: 'Administrador',
}

export class AuthError extends Error {}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

async function loginMock({ usuario, password }) {
  await wait(700)
  // Se acepta también el correo, que era el dato de prueba de las entregas anteriores.
  const nombre = usuario.toLowerCase()
  const coincide = nombre === DEMO_USER.usuario || nombre === DEMO_USER.correo
  if (!coincide || password !== DEMO_USER.password) {
    throw new AuthError('Usuario o contraseña incorrectos.')
  }
  return {
    access: 'mock-access',
    refresh: 'mock-refresh',
    usuario: {
      id: 1,
      usuario: DEMO_USER.usuario,
      correo: DEMO_USER.correo,
      nombre: DEMO_USER.nombre,
      rol: 'admin',
      esGlobal: true,
      local: 1,
    },
  }
}

/** Datos del usuario (nombre, rol, local). Si /perfil/ falla, se sigue sin ellos. */
async function leerPerfil(access) {
  try {
    const r = await fetch(`${API_URL}${RUTAS_AUTH.perfil}`, { headers: { Authorization: `Bearer ${access}` } })
    if (!r.ok) return {}
    const p = await r.json()
    return {
      id: p.id,
      usuario: p.nombre_usuario,
      nombre: [p.nombre, p.apellido].filter(Boolean).join(' ') || p.nombre_usuario,
      correo: p.correo || undefined,
      rol: p.rol,
      esGlobal: Boolean(p.es_global),
      local: p.local ?? undefined,
    }
  } catch {
    return {}
  }
}

/** Lee el payload de un JWT sin validar la firma (eso lo hace el backend). */
function decodeJwt(token) {
  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    return JSON.parse(atob(payload))
  } catch {
    return {}
  }
}

async function loginApi({ usuario, password }) {
  let response
  try {
    response = await fetch(`${API_URL}${RUTAS_AUTH.login}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // SimpleJWT espera el USERNAME_FIELD del modelo core.Usuario: "nombre_usuario".
      body: JSON.stringify({ nombre_usuario: usuario, password }),
    })
  } catch {
    throw new AuthError('No se pudo conectar con el servidor.')
  }

  if (response.status === 400 || response.status === 401) {
    throw new AuthError('Usuario o contraseña incorrectos.')
  }
  if (!response.ok) {
    throw new AuthError('El servidor no respondió como se esperaba. Intenta de nuevo.')
  }

  const { access, refresh } = await response.json()
  const perfil = await leerPerfil(access)
  return {
    access,
    refresh,
    usuario: {
      usuario,
      id: decodeJwt(access).user_id,
      esGlobal: false,
      ...perfil,
    },
  }
}

export async function login(credentials) {
  const session = USE_MOCK ? await loginMock(credentials) : await loginApi(credentials)
  saveSession(session)
  if (USE_MOCK) anotarAccion({ modulo: 'identity', entidad: 'Usuario', entidad_id: 1, accion: 'login' })
  return session
}

export function logout() {
  clearSession()
}

export { saveSession, loadSession }

export const isMock = USE_MOCK
