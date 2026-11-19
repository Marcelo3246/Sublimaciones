import { useRef, useState } from 'react'
import TextField from '../../components/TextField.jsx'
import PasswordField from '../../components/PasswordField.jsx'
import Button from '../../components/Button.jsx'
import FormMessage from '../../components/FormMessage.jsx'
import userIcon from '../../assets/icons/user.svg'
import { AuthError, login } from './api.js'

export default function LoginForm({ onLogin }) {
  const [usuario, setUsuario] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState({})
  const [message, setMessage] = useState(null)
  const [loading, setLoading] = useState(false)

  const usuarioRef = useRef(null)
  const passwordRef = useRef(null)

  async function handleSubmit(event) {
    event.preventDefault()
    if (loading) return

    const nextErrors = {
      usuario: usuario.trim() ? null : 'Escribe tu usuario.',
      password: password ? null : 'Escribe tu contraseña.',
    }
    setErrors(nextErrors)
    if (nextErrors.usuario) return usuarioRef.current?.focus()
    if (nextErrors.password) return passwordRef.current?.focus()

    setMessage(null)
    setLoading(true)
    try {
      const session = await login({ usuario: usuario.trim(), password })
      onLogin(session)
    } catch (error) {
      const text = error instanceof AuthError ? error.message : 'Ocurrió un error inesperado. Intenta de nuevo.'
      setMessage({ tone: 'error', text })
      setPassword('')
      passwordRef.current?.focus()
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="auth-form" onSubmit={handleSubmit} noValidate>
      <TextField
        ref={usuarioRef}
        label="Usuario"
        icon={userIcon}
        type="text"
        name="usuario"
        autoComplete="username"
        autoCapitalize="none"
        spellCheck={false}
        placeholder="Tu nombre de usuario"
        value={usuario}
        onChange={(e) => {
          setUsuario(e.target.value)
          if (errors.usuario) setErrors((prev) => ({ ...prev, usuario: null }))
        }}
        error={errors.usuario}
        autoFocus
      />

      <PasswordField
        ref={passwordRef}
        label="Contraseña"
        name="password"
        autoComplete="current-password"
        value={password}
        onChange={(e) => {
          setPassword(e.target.value)
          if (errors.password) setErrors((prev) => ({ ...prev, password: null }))
        }}
        error={errors.password}
        labelAside={
          <button
            type="button"
            className="text-link"
            onClick={() =>
              setMessage({ tone: 'info', text: 'Pide al administrador que restablezca tu contraseña.' })
            }
          >
            ¿La olvidaste?
          </button>
        }
      />

      {message && <FormMessage tone={message.tone}>{message.text}</FormMessage>}

      <Button type="submit" loading={loading} loadingText="Ingresando…">
        Ingresar
      </Button>
    </form>
  )
}
