/**
 * Base de datos simulada en el navegador (solo para VITE_API_MOCK=true).
 *
 * Cada módulo registra su colección con datos de ejemplo (semilla.js de cada
 * feature). Todo se guarda en localStorage, así los cambios sobreviven a una
 * recarga. Para volver a los datos de ejemplo: botón "Restablecer datos de
 * ejemplo" del menú de usuario, o borrar la clave CLAVE en localStorage.
 *
 * Nada de este archivo se usa cuando el módulo apunta al backend real.
 */

const CLAVE = 'sublimacion.mock.v1'

function cargar() {
  try {
    const guardado = JSON.parse(localStorage.getItem(CLAVE))
    if (guardado?.colecciones) return guardado
  } catch {
    /* sin almacenamiento: se arranca de cero */
  }
  return { colecciones: {}, secuencias: {} }
}

let estado = cargar()

function guardar() {
  try {
    localStorage.setItem(CLAVE, JSON.stringify(estado))
  } catch {
    /* si no se puede guardar, los cambios duran hasta recargar */
  }
}

const copiar = (valor) => (valor == null ? valor : JSON.parse(JSON.stringify(valor)))

/** Registra una colección con sus datos de ejemplo (solo la primera vez). */
export function registrar(nombre, semilla = []) {
  if (estado.colecciones[nombre]) return
  const filas = typeof semilla === 'function' ? semilla() : semilla
  estado.colecciones[nombre] = copiar(filas)
  estado.secuencias[nombre] = filas.reduce((max, f) => Math.max(max, Number(f.id) || 0), 0)
  guardar()
}

export function todos(nombre) {
  return copiar(estado.colecciones[nombre] ?? [])
}

export function obtener(nombre, id) {
  return copiar((estado.colecciones[nombre] ?? []).find((f) => String(f.id) === String(id)) ?? null)
}

export function insertar(nombre, datos) {
  estado.colecciones[nombre] ??= []
  const id = (estado.secuencias[nombre] ?? 0) + 1
  estado.secuencias[nombre] = id
  const momento = new Date().toISOString()
  const fila = { activo: true, ...copiar(datos), id, creado_en: momento, actualizado_en: momento }
  estado.colecciones[nombre].push(fila)
  guardar()
  return copiar(fila)
}

export function actualizar(nombre, id, cambios) {
  const filas = estado.colecciones[nombre] ?? []
  const indice = filas.findIndex((f) => String(f.id) === String(id))
  if (indice === -1) return null
  filas[indice] = { ...filas[indice], ...copiar(cambios), id: filas[indice].id, actualizado_en: new Date().toISOString() }
  guardar()
  return copiar(filas[indice])
}

/** Borra todos los datos simulados y recarga la página con los de ejemplo. */
export function reiniciarDatos() {
  try {
    localStorage.removeItem(CLAVE)
  } catch {
    /* nada que borrar */
  }
  estado = { colecciones: {}, secuencias: {} }
  window.location.reload()
}

/** Simula la demora de la red para que se vean los estados de carga. */
export const esperar = (ms = 220) => new Promise((resolve) => setTimeout(resolve, ms))
