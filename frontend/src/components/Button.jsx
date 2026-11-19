import './Button.css'

/**
 * Botón del sistema. `variant`: "primary" (morado) o "secondary" (blanco con borde).
 * `inline`: ancho según el texto en vez de ocupar toda la fila.
 * Con `loading` muestra un indicador y bloquea nuevos clics.
 */
export default function Button({
  variant = 'primary',
  inline = false,
  loading = false,
  loadingText,
  children,
  className = '',
  disabled,
  ...props
}) {
  const clases = ['button', variant === 'secondary' && 'button--secondary', inline && 'button--inline', className]
    .filter(Boolean)
    .join(' ')

  return (
    <button className={clases} disabled={loading || disabled} aria-busy={loading || undefined} {...props}>
      {loading && <span className="button__spinner" aria-hidden="true" />}
      {loading && loadingText ? loadingText : children}
    </button>
  )
}
