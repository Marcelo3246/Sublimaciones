import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import LoginForm from './LoginForm.jsx'
import { useSesion } from './Sesion.jsx'
import './Login.css'

export default function Login() {
  const { sesion, iniciarSesion } = useSesion()
  const navigate = useNavigate()
  const location = useLocation()
  const destino = location.state?.desde || '/'

  // Si ya hay sesión no tiene sentido mostrar el login.
  if (sesion) return <Navigate to={destino} replace />

  return (
    <main className="login-page">
      <title>Iniciar sesión · Sublimación</title>
      <section className="auth-card" aria-labelledby="auth-title">
        <div className="auth-header">
          <h1 id="auth-title" className="auth-header__title">
            Iniciar sesión
          </h1>
        </div>
        <LoginForm
          onLogin={(nueva) => {
            iniciarSesion(nueva)
            navigate(destino, { replace: true })
          }}
        />
      </section>
    </main>
  )
}
