import Button from './Button.jsx'
import EstadoVacio from './EstadoVacio.jsx'
import './ContenidoConsulta.css'

/**
 * Muestra "Cargando…", el error con botón de reintentar, el mensaje de vacío
 * o el contenido, según el estado de una consulta (hooks/useConsulta).
 *   <ContenidoConsulta consulta={consulta} vacio="No hay clientes.">
 *     {(filas) => <table>…</table>}
 *   </ContenidoConsulta>
 */
export default function ContenidoConsulta({ consulta, vacio = 'No hay registros.', esVacio, children }) {
  const { cargando, error, datos, recargar } = consulta

  if (error && !datos) {
    return (
      <div className="error-carga" role="alert">
        <span>{error.message || 'No se pudo cargar la información.'}</span>
        <Button type="button" variant="secondary" inline onClick={recargar}>
          Reintentar
        </Button>
      </div>
    )
  }
  if (cargando && !datos) return <p className="cargando">Cargando…</p>

  const sinDatos = esVacio ? esVacio(datos) : Array.isArray(datos) && datos.length === 0
  if (sinDatos) return <EstadoVacio texto={vacio} />

  return children(datos)
}
