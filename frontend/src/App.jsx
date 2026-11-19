import { Navigate, Route, Routes } from 'react-router-dom'
import { RutaProtegida } from './features/auth/Sesion.jsx'
import Layout from './components/Layout.jsx'
import EstadoVacio from './components/EstadoVacio.jsx'

// Cada feature declara sus páginas en src/features/<nombre>/rutas.jsx y aquí
// se cargan solas. Así cada feature se puede subir a GitHub por separado sin
// tocar este archivo:
//   export const rutas = [{ path: '/clientes', element: <Clientes /> }]
// Opciones de cada ruta: publica (sin sesión) y soloAdmin (solo es_global).
const archivos = import.meta.glob('./features/*/rutas.jsx', { eager: true })
const RUTAS = Object.values(archivos).flatMap((modulo) => modulo.rutas ?? [])

// Si todavía no se subió el dashboard, "/" muestra una página vacía.
const HAY_INICIO = RUTAS.some((r) => r.path === '/')

export default function App() {
  return (
    <Routes>
      {RUTAS.map((r) => (
        <Route
          key={r.path}
          path={r.path}
          element={r.publica ? r.element : <RutaProtegida soloAdmin={r.soloAdmin}>{r.element}</RutaProtegida>}
        />
      ))}
      {!HAY_INICIO && (
        <Route
          path="/"
          element={
            <RutaProtegida>
              <Layout activa="dashboard" titulo="Inicio">
                <EstadoVacio texto="Elige una sección del menú." />
              </Layout>
            </RutaProtegida>
          }
        />
      )}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
