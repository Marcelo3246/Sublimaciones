/**
 * Nombres de las colecciones simuladas. Se comparten porque algunos módulos
 * leen datos de otros en modo simulado (el dashboard y los reportes calculan
 * sus cifras a partir de ventas, compras e inventario).
 *
 * Con el backend real esto no se usa: cada cálculo lo hace Django.
 */
export const COL = {
  categorias: 'categorias',
  unidades: 'unidades',
  productos: 'productos',
  materiales: 'materiales',
  movimientos: 'movimientos',
  clientes: 'clientes',
  pedidos: 'pedidos',
  proveedores: 'proveedores',
  ordenesCompra: 'ordenes_compra',
  usuarios: 'usuarios',
  roles: 'roles',
  acciones: 'acciones',
}
