/**
 * Dashboard — backend: app reports (no tiene tablas propias, calcula a partir
 * de sales, purchasing e inventory).
 *
 *   GET /reports/dashboard/  ->
 *   {
 *     resumen: { ingresosHoy, ventasHoy, ingresosMes, ventasMes, pedidosPorEntregar,
 *                vencenManana, comprasMes, cantidadComprasMes, proveedoresMes },
 *     ingresosDiarios: { "28": 1800, "29": 1400 },      // día del mes actual -> ingresos
 *     proximasEntregas: [{ id, codigo, cliente, descripcion, entrega, urgente }],
 *     stockMateriaPrima: [{ id, descripcion, detalle, cantidad }],  // 3 con menos stock
 *     stockProductos:    [{ id, descripcion, detalle, cantidad }],
 *     movimientos:       [{ id, descripcion, detalle, cantidad }]   // 3 últimos
 *   }
 *
 * En modo simulado esas cifras se calculan aquí con los datos de ejemplo de
 * los demás módulos.
 */
import { usaMock } from '../../api/config.js'
import { pedir } from '../../api/cliente.js'
import { COL } from '../../api/mock/colecciones.js'
import { esperar, todos } from '../../api/mock/db.js'
import { aFecha, diasHasta, entrega, hora, isoDia } from '../../utils/formato.js'

// Pedidos que cuentan como venta (ya confirmados y no anulados)
const ES_VENTA = ['confirmado', 'en_produccion', 'listo', 'entregado', 'facturado']
const POR_ENTREGAR = ['confirmado', 'en_produccion', 'listo']
const COMPRA_VALIDA = ['confirmada', 'recibida']

const TEXTO_MOVIMIENTO = {
  entrada_compra: 'Entrada por compra',
  salida_venta: 'Salida por venta',
  ajuste: 'Ajuste manual',
  desperdicio: 'Baja por desperdicio',
}

const activos = (filas) => filas.filter((f) => f.activo !== false)

function calcularMock() {
  const hoy = new Date()
  const hoyIso = isoDia(hoy)
  const mismoMes = (valor) => {
    const f = aFecha(valor)
    return f && f.getMonth() === hoy.getMonth() && f.getFullYear() === hoy.getFullYear()
  }

  const clientes = Object.fromEntries(todos(COL.clientes).map((c) => [c.id, c.nombre]))
  const categorias = Object.fromEntries(todos(COL.categorias).map((c) => [c.id, c.nombre]))
  const pedidos = todos(COL.pedidos)
  const ventas = pedidos.filter((p) => ES_VENTA.includes(p.estado) && p.confirmado_en)
  const ventasHoy = ventas.filter((p) => isoDia(p.confirmado_en) === hoyIso)
  const ventasMes = ventas.filter((p) => mismoMes(p.confirmado_en))
  const suma = (lista) => lista.reduce((s, p) => s + Number(p.total), 0)

  const pendientes = pedidos.filter((p) => POR_ENTREGAR.includes(p.estado))
  const compras = todos(COL.ordenesCompra).filter((o) => COMPRA_VALIDA.includes(o.estado) && mismoMes(o.creado_en))

  const ingresosDiarios = {}
  ventasMes.forEach((p) => {
    const dia = aFecha(p.confirmado_en).getDate()
    ingresosDiarios[dia] = (ingresosDiarios[dia] || 0) + Number(p.total)
  })

  const menorStock = (filas) =>
    activos(filas)
      .sort((a, b) => Number(a.cantidad_disponible) - Number(b.cantidad_disponible))
      .slice(0, 3)
      .map((f) => ({ id: f.id, descripcion: f.nombre, detalle: categorias[f.categoria] ?? '', cantidad: Number(f.cantidad_disponible) }))

  const describir = (lineas = []) =>
    lineas.length === 1 ? `${lineas[0].cantidad} × ${lineas[0].descripcion}` : `${lineas[0]?.descripcion ?? ''} y ${lineas.length - 1} más`

  return {
    resumen: {
      ingresosHoy: suma(ventasHoy),
      ventasHoy: ventasHoy.length,
      ingresosMes: suma(ventasMes),
      ventasMes: ventasMes.length,
      pedidosPorEntregar: pendientes.length,
      vencenManana: pendientes.filter((p) => diasHasta(p.fecha_entrega) === 1).length,
      comprasMes: compras.reduce((s, o) => s + Number(o.total), 0),
      cantidadComprasMes: compras.length,
      proveedoresMes: new Set(compras.map((o) => o.proveedor)).size,
    },
    ingresosDiarios,
    proximasEntregas: pendientes
      .filter((p) => p.fecha_entrega)
      .sort((a, b) => a.fecha_entrega.localeCompare(b.fecha_entrega))
      .slice(0, 4)
      .map((p) => ({
        id: p.id,
        codigo: p.codigo_pedido,
        cliente: clientes[p.cliente] ?? 'Venta de mostrador',
        descripcion: describir(p.lineas),
        entrega: entrega(p.fecha_entrega),
        urgente: diasHasta(p.fecha_entrega) <= 1,
      })),
    stockMateriaPrima: menorStock(todos(COL.materiales)),
    stockProductos: menorStock(todos(COL.productos)),
    movimientos: todos(COL.movimientos)
      .sort((a, b) => String(b.creado_en).localeCompare(String(a.creado_en)))
      .slice(0, 3)
      .map((m) => ({
        id: m.id,
        descripcion: m.item_nombre,
        detalle: `${TEXTO_MOVIMIENTO[m.tipo_movimiento] ?? 'Movimiento'}, ${hora(m.creado_en)}`,
        cantidad: Number(m.cantidad),
      })),
  }
}

export async function obtenerDashboard() {
  if (usaMock('dashboard')) {
    await esperar()
    return calcularMock()
  }
  return pedir('/reports/dashboard/')
}
