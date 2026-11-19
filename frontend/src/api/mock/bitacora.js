/**
 * En modo simulado, cada alta, cambio o baja queda anotada en la colección
 * "acciones" para que el módulo de Auditoría tenga qué mostrar.
 * En el backend real esto lo hace core.audit (BitacoraAccion).
 */

import { insertar } from './db.js'
import { COL } from './colecciones.js'
import { loadSession } from '../sesion.js'

export function anotarAccion({ modulo, entidad, entidad_id = null, accion, estado_anterior = null, estado_nuevo = null }) {
  const usuario = loadSession()?.usuario
  insertar(COL.acciones, {
    usuario: usuario?.id ?? null,
    usuario_nombre: usuario?.nombre || usuario?.correo || 'Sistema',
    modulo,
    entidad,
    entidad_id,
    accion,
    estado_anterior,
    estado_nuevo,
    direccion_ip: '127.0.0.1',
  })
}
