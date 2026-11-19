import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * Ejecuta una función async (normalmente de un api.js) y guarda su estado.
 *   const consulta = useConsulta(() => clientesApi.listar({ q }), [q])
 *   consulta.cargando / consulta.error / consulta.datos / consulta.recargar()
 */
export function useConsulta(funcion, dependencias = []) {
  const [estado, setEstado] = useState({ cargando: true, error: null, datos: null })
  const ultima = useRef(0)
  const funcionRef = useRef(funcion)
  funcionRef.current = funcion

  const ejecutar = useCallback(async () => {
    const numero = ++ultima.current
    setEstado((previo) => ({ ...previo, cargando: true, error: null }))
    try {
      const datos = await funcionRef.current()
      // Si mientras tanto empezó otra consulta, esta respuesta ya no sirve.
      if (numero === ultima.current) setEstado({ cargando: false, error: null, datos })
    } catch (error) {
      if (numero === ultima.current) setEstado((previo) => ({ ...previo, cargando: false, error }))
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencias)

  useEffect(() => {
    ejecutar()
  }, [ejecutar])

  return { ...estado, recargar: ejecutar }
}
