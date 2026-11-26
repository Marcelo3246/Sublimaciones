import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../../../hooks/useAuth";

/**
 * Envuelve las rutas que necesitan sesión. Sin sesión manda al login y
 * recuerda la página pedida para volver a ella después de ingresar.
 */
export function RutaProtegida() {
  const access = useAuth((s) => s.access);
  const location = useLocation();

  if (!access) return <Navigate to="/login" replace state={{ desde: location.pathname }} />;
  return <Outlet />;
}
