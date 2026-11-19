import { useEffect, useState } from 'react'

/** Devuelve el valor recién cuando dejó de cambiar `ms` milisegundos (para no llamar a la API en cada tecla). */
export function useDiferido(valor, ms = 300) {
  const [diferido, setDiferido] = useState(valor)
  useEffect(() => {
    const t = setTimeout(() => setDiferido(valor), ms)
    return () => clearTimeout(t)
  }, [valor, ms])
  return diferido
}
