// Descarga una tabla como CSV que Excel abre bien en español
// (separador ";" y marca BOM para que respete las tildes).

const celda = (valor) => {
  const texto = valor === null || valor === undefined ? '' : String(valor)
  return /[";\n]/.test(texto) ? `"${texto.replace(/"/g, '""')}"` : texto
}

/**
 * descargarCsv('ventas.csv', [{ titulo: 'Producto', valor: (f) => f.nombre }, …], filas)
 */
export function descargarCsv(nombre, columnas, filas) {
  const lineas = [
    columnas.map((c) => celda(c.titulo)).join(';'),
    ...filas.map((f) => columnas.map((c) => celda(c.valor(f))).join(';')),
  ]
  const blob = new Blob(['﻿' + lineas.join('\r\n')], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const enlace = document.createElement('a')
  enlace.href = url
  enlace.download = nombre
  document.body.appendChild(enlace)
  enlace.click()
  enlace.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

/** Número con coma decimal para Excel en español: 12.5 -> "12,50" */
export const numeroCsv = (n) => (Number(n) || 0).toFixed(2).replace('.', ',')
