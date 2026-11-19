import { forwardRef, useId } from 'react'
import './TextField.css'

/**
 * Campo de texto con ícono a la izquierda, acción opcional a la derecha
 * (p. ej. mostrar contraseña) y mensaje de error accesible.
 */
const TextField = forwardRef(function TextField(
  { label, icon, error, labelAside, trailing, className = '', ...inputProps },
  ref,
) {
  const id = useId()
  const errorId = `${id}-error`

  return (
    <div className={`field ${className}`}>
      <div className="field__label-row">
        <label className="field__label" htmlFor={id}>
          {label}
        </label>
        {labelAside}
      </div>

      <div className={`field__control${error ? ' field__control--invalid' : ''}`}>
        {icon && <img className="field__icon" src={icon} alt="" width="16" height="16" />}
        <input
          ref={ref}
          id={id}
          className="field__input"
          aria-invalid={error ? 'true' : undefined}
          aria-describedby={error ? errorId : undefined}
          {...inputProps}
        />
        {trailing}
      </div>

      {error && (
        <p id={errorId} className="field__error">
          {error}
        </p>
      )}
    </div>
  )
})

export default TextField
