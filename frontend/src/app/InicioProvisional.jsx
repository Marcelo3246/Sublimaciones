import { useQueryClient } from "@tanstack/react-query";
import { Button } from "../components/Button";
import { useAuth } from "../hooks/useAuth";
import { cerrarSesion } from "../services/auth";

/**
 * Página de inicio provisional: confirma que la sesión quedó iniciada.
 * Se reemplaza por el dashboard (features/reportes) cuando se integre.
 */
export function InicioProvisional() {
  const usuario = useAuth((s) => s.usuario);
  const queryClient = useQueryClient();
  const nombre = [usuario?.nombre, usuario?.apellido].filter(Boolean).join(" ") || usuario?.nombre_usuario;

  function salir() {
    cerrarSesion();
    queryClient.clear();
  }

  return (
    <main className="flex min-h-full items-center justify-center px-4 py-12">
      <title>Inicio · DLL Sublimados</title>
      <section className="w-full max-w-[400px] rounded-tarjeta border border-borde bg-superficie p-8 text-center shadow-tarjeta">
        <h1 className="text-base font-medium">Hola, {nombre}</h1>
        <p className="mt-1 mb-6 text-texto-secundario">
          Sesión iniciada{usuario?.rol ? ` como ${usuario.rol}` : ""}.
        </p>
        <Button variant="secondary" onClick={salir}>
          Cerrar sesión
        </Button>
      </section>
    </main>
  );
}
