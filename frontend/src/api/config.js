/**
 * Configuración de la conexión con el backend Django.
 *
 * VITE_API_URL     URL base de la API (sin barra final).
 * VITE_API_MOCK    true = cada módulo usa datos simulados en el navegador.
 * VITE_API_REALES  Lista de módulos que ya usan el backend real aunque el resto
 *                  siga simulado. Ej.: VITE_API_REALES=clientes,proveedores
 *
 * Los nombres de módulo son los de src/features (clientes, proveedores,
 * inventario, ventas, compras, reportes, historial, auditoria, usuarios, dashboard).
 */

export const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1').replace(/\/$/, '')

const MOCK_GLOBAL = import.meta.env.VITE_API_MOCK !== 'false'

const REALES = (import.meta.env.VITE_API_REALES || '')
  .split(',')
  .map((m) => m.trim())
  .filter(Boolean)

/** true si el módulo debe responder con datos simulados. */
export function usaMock(modulo) {
  return MOCK_GLOBAL && !REALES.includes(modulo)
}

/**
 * Rutas de autenticación (relativas a API_URL). Siguen backend/config/urls.py y
 * backend/apps/core/urls.py del PR #3 del repo oficial. Si cambian, se ajustan aquí.
 */
export const RUTAS_AUTH = {
  login: '/auth/token/',
  refresh: '/auth/token/refresh/',
  perfil: '/core/perfil/',
}

/** Local (sucursal) que se envía al crear pedidos, compras y movimientos. */
export const LOCAL_POR_DEFECTO = Number(import.meta.env.VITE_LOCAL_ID || 1)
