import { forwardRef, useState } from 'react'
import TextField from './TextField.jsx'
import lockIcon from '../assets/icons/lock.svg'
import eyeIcon from '../assets/icons/eye.svg'
import eyeOffIcon from '../assets/icons/eye-off.svg'

/** Campo de contraseña con botón para mostrar u ocultar lo escrito. */
const PasswordField = forwardRef(function PasswordField(props, ref) {
  const [visible, setVisible] = useState(false)

  return (
    <TextField
      ref={ref}
      icon={lockIcon}
      type={visible ? 'text' : 'password'}
      trailing={
        <button
          type="button"
          className="icon-button"
          aria-label={visible ? 'Ocultar contraseña' : 'Mostrar contraseña'}
          aria-pressed={visible}
          onClick={() => setVisible((v) => !v)}
        >
          <img src={visible ? eyeOffIcon : eyeIcon} alt="" width="16" height="16" />
        </button>
      }
      {...props}
    />
  )
})

export default PasswordField
