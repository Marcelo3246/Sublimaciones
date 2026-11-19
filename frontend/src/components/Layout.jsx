import { Link } from 'react-router-dom'
import Sidebar from './Sidebar/Sidebar.jsx'
import './Layout.css'

/**
 * Estructura de todas las páginas internas: menú lateral + encabezado + contenido.
 *   <Layout activa="clientes" titulo="Clientes" acciones={<Button>Nuevo cliente</Button>}>
 * `migas`: [{ texto: 'Ventas y pedidos', ruta: '/ventas' }] para subpáginas.
 */
export default function Layout({ activa, titulo, acciones, migas, children }) {
  return (
    <div className="layout">
      <title>{`${titulo} · Sublimación`}</title>
      <Sidebar activa={activa} />

      <main className="contenido">
        <header className="cabecera">
          <div>
            {migas && (
              <ol className="migas" aria-label="Ubicación">
                {migas.map((m) => (
                  <li key={m.texto}>{m.ruta ? <Link to={m.ruta}>{m.texto}</Link> : m.texto}</li>
                ))}
              </ol>
            )}
            <h1>{titulo}</h1>
          </div>
          {acciones && <div className="acciones">{acciones}</div>}
        </header>

        {children}
      </main>
    </div>
  )
}
