import { forwardRef, useId } from 'react'
import './TextField.css'
import './Campo.css'

/**
 * Campo de formulario con etiqueta y error accesible.
 *   <Campo label="Nombre" value={...} onChange={...} error={...} />
 *   <Campo as="select" label="Categoría">{opciones}</Campo>
 *   <Campo as="textarea" label="Notas" opcional />
 */
const Campo = forwardRef(function Campo(
  { label, error, as: Control = 'input', opcional = false, className = '', controlClassName = '', children, ...props },
  ref,
) {
  const id = useId()
  const errorId = `${id}-error`

  return (
    <div className={`campo ${className}`}>
      <label className="field__label" htmlFor={id}>
        {label}
        {opcional && <span> (opcional)</span>}
      </label>
      <Control
        ref={ref}
        id={id}
        className={`control${error ? ' control--invalido' : ''} ${controlClassName}`}
        aria-invalid={error ? 'true' : undefined}
        aria-describedby={error ? errorId : undefined}
        {...props}
      >
        {children}
      </Control>
      {error && (
        <p id={errorId} className="field__error">
          {error}
        </p>
      )}
    </div>
  )
})

export default Campo
