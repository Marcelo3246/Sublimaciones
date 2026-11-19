/**
 * Cliente HTTP único para hablar con el backend Django + DRF.
 *
 * - Agrega el token JWT (Authorization: Bearer ...).
 * - Si el token venció (401), pide uno nuevo con el refresh y repite la llamada.
 * - Convierte los errores de DRF en ApiError con un mensaje legible y los
 *   errores por campo en `error.campos` (para mostrarlos en los formularios).
 */

import { API_URL, RUTAS_AUTH } from './config.js'
import { EVENTO_SESION_EXPIRADA, clearSession, loadSession, updateTokens } from './sesion.js'

export class ApiError extends Error {
  constructor(message, { status = 0, campos = {}, datos = null } = {}) {
    super(message)
    this.status = status
    this.campos = campos
    this.datos = datos
  }
}

function armarUrl(ruta, params) {
  const url = ruta.startsWith('http') ? ruta : `${API_URL}${ruta}`
  if (!params) return url
  const query = new URLSearchParams()
  Object.entries(params).forEach(([clave, valor]) => {
    if (valor === undefined || valor === null || valor === '') return
    query.append(clave, valor)
  })
  const texto = query.toString()
  return texto ? `${url}${url.includes('?') ? '&' : '?'}${texto}` : url
}

/** DRF responde { detail } o { campo: ["mensaje"] }; se arma un texto y un mapa por campo. */
function leerError(datos, status) {
  const campos = {}
  let mensaje = ''

  if (datos && typeof datos === 'object') {
    if (typeof datos.detail === 'string') mensaje = datos.detail
    Object.entries(datos).forEach(([campo, valor]) => {
      if (campo === 'detail') return
      const texto = Array.isArray(valor) ? valor.join(' ') : typeof valor === 'string' ? valor : ''
      if (!texto) return
      if (campo === 'non_field_errors') mensaje = mensaje || texto
      else campos[campo] = texto
    })
    if (!mensaje && Object.keys(campos).length) mensaje = 'Revisa los datos marcados.'
  }

  if (!mensaje) {
    if (status === 403) mensaje = 'No tienes permiso para hacer esto.'
    else if (status === 404) mensaje = 'No se encontró el registro.'
    else if (status >= 500) mensaje = 'El servidor tuvo un problema. Intenta de nuevo.'
    else mensaje = 'El servidor no respondió como se esperaba.'
  }
  return new ApiError(mensaje, { status, campos, datos })
}

let refrescando = null

/** Pide un access nuevo con el refresh guardado. Devuelve true si lo consiguió. */
async function refrescarToken() {
  const refresh = loadSession()?.refresh
  if (!refresh) return false

  // Si varias llamadas reciben 401 a la vez, se hace un solo refresh.
  refrescando ??= fetch(`${API_URL}${RUTAS_AUTH.refresh}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  })
    .then(async (r) => {
      if (!r.ok) return false
      updateTokens(await r.json())
      return true
    })
    .catch(() => false)
    .finally(() => {
      refrescando = null
    })

  return refrescando
}

function sesionExpirada() {
  clearSession()
  window.dispatchEvent(new Event(EVENTO_SESION_EXPIRADA))
}

/**
 * Hace una llamada a la API.
 *   pedir('/sales/clientes/', { params: { search: 'ana' } })
 *   pedir('/sales/clientes/', { metodo: 'POST', datos: { nombre: 'Ana' } })
 */
export async function pedir(ruta, { metodo = 'GET', datos, params, auth = true, reintento = true } = {}) {
  const headers = { Accept: 'application/json' }
  if (datos !== undefined) headers['Content-Type'] = 'application/json'
  const access = auth ? loadSession()?.access : null
  if (access) headers.Authorization = `Bearer ${access}`

  let respuesta
  try {
    respuesta = await fetch(armarUrl(ruta, params), {
      method: metodo,
      headers,
      body: datos !== undefined ? JSON.stringify(datos) : undefined,
    })
  } catch {
    throw new ApiError('No se pudo conectar con el servidor.')
  }

  if (respuesta.status === 401 && auth) {
    if (reintento && (await refrescarToken())) {
      return pedir(ruta, { metodo, datos, params, auth, reintento: false })
    }
    sesionExpirada()
    throw new ApiError('Tu sesión venció. Vuelve a ingresar.', { status: 401 })
  }

  if (respuesta.status === 204) return null

  const cuerpo = await respuesta.json().catch(() => null)
  if (!respuesta.ok) throw leerError(cuerpo, respuesta.status)
  return cuerpo
}

/**
 * Lee un listado completo. DRF pagina de a 25 (PageNumberPagination):
 * se siguen los enlaces `next` hasta traer todo (máximo 40 páginas).
 */
export async function pedirLista(ruta, params) {
  let respuesta = await pedir(ruta, { params })
  if (Array.isArray(respuesta)) return respuesta

  const filas = [...(respuesta?.results ?? [])]
  let paginas = 1
  while (respuesta?.next && paginas < 40) {
    respuesta = await pedir(respuesta.next)
    filas.push(...(respuesta?.results ?? []))
    paginas += 1
  }
  return filas
}
