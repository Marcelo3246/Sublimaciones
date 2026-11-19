/**
 * Movimientos de stock en modo simulado: suman o restan la cantidad del
 * producto o materia prima y dejan el registro en "movimientos".
 *
 * Con el backend real, ventas y compras NO llaman a esto: el backend mueve el
 * stock al confirmar una venta o recibir una compra (inventory.MovimientoStock).
 */

import { actualizar, insertar, obtener } from './db.js'
import { COL } from './colecciones.js'
import { loadSession } from '../sesion.js'

const COLECCION_DE = { producto: COL.productos, material: COL.materiales }

/**
 * @param {object} m
 * @param {'producto'|'material'} m.tipo_item
 * @param {number} m.item_id
 * @param {number} m.cantidad  positiva = entrada, negativa = salida
 * @param {string} m.tipo_movimiento  entrada_compra, salida_venta, ajuste, desperdicio...
 */
export function moverStock({ tipo_item, item_id, cantidad, tipo_movimiento, motivo = '' }) {
  const coleccion = COLECCION_DE[tipo_item]
  const item = obtener(coleccion, item_id)
  if (!item) return null

  const nueva = Math.max(0, Number(item.cantidad_disponible || 0) + Number(cantidad))
  actualizar(coleccion, item_id, { cantidad_disponible: Math.round(nueva * 10000) / 10000 })

  const usuario = loadSession()?.usuario
  return insertar(COL.movimientos, {
    tipo_movimiento,
    tipo_item,
    item_id,
    item_nombre: item.nombre,
    um: item.um || 'und',
    cantidad: Number(cantidad),
    motivo,
    usuario_nombre: usuario?.nombre || usuario?.correo || 'Sistema',
  })
}
