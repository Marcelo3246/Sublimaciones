import './FormMessage.css'

/** Mensaje general del formulario (error del servidor, aviso, confirmación). */
export default function FormMessage({ tone = 'info', children }) {
  return (
    <p className={`form-message form-message--${tone}`} role={tone === 'error' ? 'alert' : 'status'}>
      {children}
    </p>
  )
}
