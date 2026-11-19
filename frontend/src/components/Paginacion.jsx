import { useEffect, useState } from 'react'
import Button from './Button.jsx'
import './Paginacion.css'

/** Divide una lista en páginas. Vuelve a la primera cuando cambia la lista. */
export function usePaginacion(filas = [], porPagina = 20) {
  const [pagina, setPagina] = useState(1)
  const total = filas.length
  const paginas = Math.max(1, Math.ceil(total / porPagina))

  useEffect(() => {
    setPagina(1)
  }, [total])

  const actual = Math.min(pagina, paginas)
  const visibles = filas.slice((actual - 1) * porPagina, actual * porPagina)
  return { visibles, pagina: actual, paginas, total, porPagina, setPagina }
}

export default function Paginacion({ pagina, paginas, total, porPagina, setPagina }) {
  if (paginas <= 1) return null
  const desde = (pagina - 1) * porPagina + 1
  const hasta = Math.min(total, pagina * porPagina)

  return (
    <nav className="paginacion" aria-label="Paginación">
      <span>
        {desde}–{hasta} de {total}
      </span>
      <div>
        <Button type="button" variant="secondary" inline disabled={pagina === 1} onClick={() => setPagina(pagina - 1)}>
          Anterior
        </Button>
        <Button type="button" variant="secondary" inline disabled={pagina === paginas} onClick={() => setPagina(pagina + 1)}>
          Siguiente
        </Button>
      </div>
    </nav>
  )
}
