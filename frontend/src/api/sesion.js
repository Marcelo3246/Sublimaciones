/**
 * Guarda los tokens y los datos del usuario que inició sesión.
 * La usan el login (features/auth) y el cliente HTTP (api/cliente.js).
 */

import { LOCAL_POR_DEFECTO } from './config.js'

const STORAGE_KEY = 'sublimacion.session'

/** Evento que se dispara cuando el backend rechaza la sesión (token vencido). */
export const EVENTO_SESION_EXPIRADA = 'sublimacion:sesion-expirada'

export function saveSession(session) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session))
  } catch {
    /* almacenamiento no disponible: la sesión dura lo que dure la pestaña */
  }
}

export function loadSession() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || null
  } catch {
    return null
  }
}

export function clearSession() {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {
    /* nada que limpiar */
  }
}

/** Actualiza solo los tokens (después de un refresh). */
export function updateTokens({ access, refresh }) {
  const actual = loadSession()
  if (!actual) return
  saveSession({ ...actual, access, refresh: refresh || actual.refresh })
}

/** Id del local con el que trabaja el usuario. */
export function localActual() {
  return loadSession()?.usuario?.local ?? LOCAL_POR_DEFECTO
}

export function usuarioActual() {
  return loadSession()?.usuario ?? null
}
