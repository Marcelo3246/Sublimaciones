import { useCallback, useState } from 'react'
import { ApiError } from '../api/cliente.js'

/**
 * Estado de un formulario: valores, errores por campo y envío.
 *   const f = useFormulario({ nombre: '' })
 *   <Campo value={f.valores.nombre} onChange={f.cambiar('nombre')} error={f.errores.nombre} />
 *   f.enviar(validar, async (valores) => api.crear(valores))
 */
export function useFormulario(inicial) {
  const [valores, setValores] = useState(inicial)
  const [errores, setErrores] = useState({})
  const [mensaje, setMensaje] = useState(null)
  const [enviando, setEnviando] = useState(false)

  const cambiar = useCallback(
    (campo) => (evento) => {
      const objetivo = evento?.target
      const valor = objetivo ? (objetivo.type === 'checkbox' ? objetivo.checked : objetivo.value) : evento
      setValores((previo) => ({ ...previo, [campo]: valor }))
      setErrores((previo) => (previo[campo] ? { ...previo, [campo]: null } : previo))
    },
    [],
  )

  const reiniciar = useCallback(
    (nuevos = inicial) => {
      setValores(nuevos)
      setErrores({})
      setMensaje(null)
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  )

  /**
   * validar(valores) devuelve { campo: 'mensaje' } con los errores (o {}).
   * guardar(valores) hace la llamada; si el backend responde errores por
   * campo, se muestran debajo de cada campo.
   */
  async function enviar(validar, guardar) {
    if (enviando) return false
    const encontrados = Object.fromEntries(Object.entries(validar(valores) || {}).filter(([, v]) => v))
    setErrores(encontrados)
    if (Object.keys(encontrados).length) return false

    setMensaje(null)
    setEnviando(true)
    try {
      await guardar(valores)
      return true
    } catch (error) {
      if (error instanceof ApiError) {
        setErrores(error.campos || {})
        setMensaje(error.message)
      } else {
        setMensaje('Ocurrió un error inesperado. Intenta de nuevo.')
      }
      return false
    } finally {
      setEnviando(false)
    }
  }

  return { valores, setValores, errores, setErrores, mensaje, setMensaje, enviando, cambiar, reiniciar, enviar }
}
