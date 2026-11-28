import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../../hooks/useAuth";
import { LoginForm } from "../components/LoginForm";

export function LoginPage() {
  const access = useAuth((s) => s.access);
  const navigate = useNavigate();
  const location = useLocation();
  const destino = location.state?.desde || "/";

  // Si ya hay sesión no tiene sentido mostrar el login.
  if (access) return <Navigate to={destino} replace />;

  return (
    <main className="flex min-h-full flex-col items-center justify-center px-4 py-12">
      <title>Iniciar sesión · DLL Sublimados</title>
      <section
        aria-labelledby="titulo-login"
        className="w-full max-w-[400px] rounded-tarjeta border border-borde bg-superficie px-8 pt-2 pb-8 shadow-tarjeta max-[420px]:px-5 max-[420px]:pb-6"
      >
        {/* Mismo estilo que la pestaña activa de Figma: sobresale 12px a cada lado */}
        <div className="-mx-3 mb-5 flex justify-center border-b border-borde max-[420px]:-mx-2">
          <h1 id="titulo-login" className="-mb-px border-b-2 border-marca px-3 py-2.5 text-sm font-medium">
            Iniciar sesión
          </h1>
        </div>

        <LoginForm onIngresar={() => navigate(destino, { replace: true })} />
      </section>
    </main>
  );
}
