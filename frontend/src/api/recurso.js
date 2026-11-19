/**
 * Recurso REST genérico (listar, obtener, crear, actualizar, desactivar)
 * que funciona igual con datos simulados o con el backend real.
 *
 * Cada feature crea los suyos en su api.js, por ejemplo:
 *
 *   export const clientesApi = crearRecurso({
 *     modulo: 'clientes',            // nombre usado en VITE_API_REALES
 *     endpoint: '/sales/clientes/',  // ruta DRF (ModelViewSet)
 *     coleccion: COL.clientes,       // colección simulada
 *     semilla: clientesEjemplo,      // datos de ejemplo
 *     entidad: 'Cliente',            // nombre para la auditoría simulada
 *     buscarEn: ['nombre', 'rif'],   // campos para el buscador simulado
 *   })
 *
 * Si el serializer del backend usa otros nombres de campo, se adaptan con
 * `desdeApi` (lo que llega) y `haciaApi` (lo que se envía) sin tocar las pantallas.
 */

import { usaMock } from './config.js'
import { pedir, pedirLista } from './cliente.js'
import { actualizar, esperar, insertar, obtener, registrar, todos } from './mock/db.js'
import { anotarAccion } from './mock/bitacora.js'

const sinTildes = (texto) =>
  String(texto ?? '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()

/** Aplica en memoria los mismos filtros que haría DRF. */
export function filtrarMock(filas, params = {}, buscarEn = []) {
  const { q, desde, hasta, campoFecha = 'creado_en', ...iguales } = params
  let resultado = filas

  Object.entries(iguales).forEach(([campo, valor]) => {
    if (valor === undefined || valor === null || valor === '') return
    // Las filas sin "activo" cuentan como activas.
    resultado = resultado.filter((f) => String(campo === 'activo' ? (f.activo ?? true) : f[campo]) === String(valor))
  })

  if (q) {
    const buscado = sinTildes(q.trim())
    resultado = resultado.filter((f) => buscarEn.some((campo) => sinTildes(f[campo]).includes(buscado)))
  }
  if (desde) resultado = resultado.filter((f) => String(f[campoFecha]).slice(0, 10) >= desde)
  if (hasta) resultado = resultado.filter((f) => String(f[campoFecha]).slice(0, 10) <= hasta)

  return resultado.sort((a, b) => Number(b.id) - Number(a.id))
}

/** Convierte los parámetros de la pantalla a los nombres que usa DRF. */
function paramsParaApi({ q, campoFecha, ...resto } = {}) {
  return { ...resto, search: q || undefined }
}

export function crearRecurso({
  modulo,
  endpoint,
  coleccion,
  semilla,
  entidad = coleccion,
  buscarEn = ['nombre'],
  desdeApi = (x) => x,
  haciaApi = (x) => x,
}) {
  if (semilla) registrar(coleccion, semilla)
  const mock = () => usaMock(modulo)
  // En la auditoría simulada el módulo se anota como lo hace el backend: nombre de la app ("sales").
  const app = endpoint.split('/').filter(Boolean)[0] ?? modulo
  const ruta = (id) => `${endpoint}${id}/`

  return {
    modulo,
    endpoint,

    /** params: { q, activo, desde, hasta, ...filtros por campo }. Por defecto solo activos. */
    async listar(params = {}) {
      const filtros = { activo: true, ...params }
      if (mock()) {
        await esperar()
        return filtrarMock(todos(coleccion), filtros, buscarEn)
      }
      const filas = await pedirLista(endpoint, paramsParaApi(filtros))
      return filas.map(desdeApi)
    },

    async obtener(id) {
      if (mock()) {
        await esperar(120)
        return obtener(coleccion, id)
      }
      return desdeApi(await pedir(ruta(id)))
    },

    async crear(datos) {
      if (mock()) {
        await esperar()
        const fila = insertar(coleccion, datos)
        anotarAccion({ modulo: app, entidad, entidad_id: fila.id, accion: 'crear', estado_nuevo: fila })
        return fila
      }
      return desdeApi(await pedir(endpoint, { metodo: 'POST', datos: haciaApi(datos) }))
    },

    async actualizar(id, cambios, accion = 'modificar') {
      if (mock()) {
        await esperar()
        const antes = obtener(coleccion, id)
        const fila = actualizar(coleccion, id, cambios)
        anotarAccion({ modulo: app, entidad, entidad_id: Number(id), accion, estado_anterior: antes, estado_nuevo: fila })
        return fila
      }
      return desdeApi(await pedir(ruta(id), { metodo: 'PATCH', datos: haciaApi(cambios) }))
    },

    /** Borrado lógico: el backend pone activo=False (modelo Auditable). */
    async desactivar(id) {
      if (mock()) {
        await esperar()
        const antes = obtener(coleccion, id)
        const fila = actualizar(coleccion, id, { activo: false })
        anotarAccion({ modulo: app, entidad, entidad_id: Number(id), accion: 'eliminar', estado_anterior: antes, estado_nuevo: fila })
        return fila
      }
      await pedir(ruta(id), { metodo: 'DELETE' })
      return null
    },

    async activar(id) {
      return this.actualizar(id, { activo: true }, 'activar')
    },
  }
}
