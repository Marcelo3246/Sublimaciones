import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import { Icono } from "../../components/Icono";
import { useAuth } from "../../hooks/useAuth";
import { useAviso } from "../../hooks/useAviso";
import { cerrarSesion } from "../../services/auth";

/**
 * Módulos del menú, en el orden de docs/08. Los que todavía no tienen
 * `ruta` muestran el aviso "en desarrollo".
 * `soloGlobal`: solo los ven los usuarios con acceso a todos los locales.
 */
const MODULOS = [
  { id: "dashboard", texto: "Dashboard", icono: "inicio", ruta: "/" },
  { id: "ventas", texto: "Ventas", icono: "ventas" },
  { id: "produccion", texto: "Producción", icono: "produccion" },
  { id: "inventario", texto: "Inventario", icono: "inventario" },
  { id: "compras", texto: "Compras", icono: "compras" },
  { id: "catalogo", texto: "Catálogo", icono: "catalogo" },
  { id: "precios", texto: "Precios", icono: "precios" },
  { id: "documentos", texto: "Documentos", icono: "documentos" },
  { id: "reportes", texto: "Reportes", icono: "reportes" },
  { id: "rrhh", texto: "Trabajadores", icono: "rrhh", soloGlobal: true },
  { id: "auditoria", texto: "Auditoría", icono: "auditoria", soloGlobal: true },
];

const EN_DESARROLLO = "Esta sección está en desarrollo y se agregará próximamente.";

const claseEnlace = (activo) =>
  `flex w-full cursor-pointer items-center gap-3 rounded-campo px-3 py-2.5 text-left transition-colors duration-150 focus-visible:outline-white ${
    activo ? "bg-marca font-medium text-white" : "hover:bg-white/8 hover:text-white"
  }`;

const claseBotonIcono =
  "grid size-10 shrink-0 cursor-pointer place-items-center rounded-campo hover:bg-white/8 hover:text-white focus-visible:outline-white";

export function Sidebar() {
  const usuario = useAuth((s) => s.usuario) ?? {};
  const mostrarAviso = useAviso((s) => s.mostrar);
  const queryClient = useQueryClient();
  // En pantallas angostas el menú se pliega bajo una barra superior.
  const [abierto, setAbierto] = useState(false);

  const nombre = [usuario.nombre, usuario.apellido].filter(Boolean).join(" ") || usuario.nombre_usuario;
  const local = usuario.es_global ? "Todos los locales" : usuario.local_info?.nombre;
  const modulos = MODULOS.filter((m) => !m.soloGlobal || usuario.es_global);

  useEffect(() => {
    if (!abierto) return;
    const alPresionar = (e) => e.key === "Escape" && setAbierto(false);
    document.addEventListener("keydown", alPresionar);
    return () => document.removeEventListener("keydown", alPresionar);
  }, [abierto]);

  function salir() {
    cerrarSesion();
    queryClient.clear();
  }

  return (
    <aside className="sticky top-0 z-40 h-screen w-[260px] shrink-0 max-[860px]:h-auto max-[860px]:w-full">
      <nav
        aria-label="Navegación principal"
        className="flex h-full flex-col overflow-y-auto bg-menu px-3.5 pt-6 pb-4 text-menu-texto max-[860px]:overflow-visible max-[860px]:px-3 max-[860px]:py-2.5"
      >
        <div className="hidden max-[860px]:flex">
          <button
            type="button"
            className={claseBotonIcono}
            onClick={() => setAbierto((a) => !a)}
            aria-expanded={abierto}
            aria-controls="menu-modulos"
            aria-label={abierto ? "Cerrar menú" : "Abrir menú"}
          >
            <Icono nombre={abierto ? "cerrar" : "menu"} tamano={22} />
          </button>
        </div>

        <div
          id="menu-modulos"
          className={`flex flex-1 flex-col max-[860px]:max-h-[calc(100vh-60px)] max-[860px]:overflow-y-auto max-[860px]:pt-3 ${
            abierto ? "" : "max-[860px]:hidden"
          }`}
        >
          <ul className="flex flex-col gap-1">
            {modulos.map((m) => (
              <li key={m.id}>
                {m.ruta ? (
                  <NavLink to={m.ruta} end className={({ isActive }) => claseEnlace(isActive)} onClick={() => setAbierto(false)}>
                    <Icono nombre={m.icono} />
                    {m.texto}
                  </NavLink>
                ) : (
                  <button type="button" className={claseEnlace(false)} onClick={() => mostrarAviso(EN_DESARROLLO)}>
                    <Icono nombre={m.icono} />
                    {m.texto}
                  </button>
                )}
              </li>
            ))}
          </ul>

          <div className="mt-auto flex items-center gap-2 border-t border-white/12 pt-4 pr-1 pl-3 max-[860px]:mt-3 max-[860px]:pt-3">
            <div className="flex min-w-0 flex-1 flex-col text-[13px] leading-[18px]">
              <strong className="truncate font-medium text-white">{nombre}</strong>
              {local && <span className="truncate">{local}</span>}
            </div>
            <button type="button" className={claseBotonIcono} onClick={salir} aria-label="Cerrar sesión" title="Cerrar sesión">
              <Icono nombre="salir" />
            </button>
          </div>
        </div>
      </nav>
    </aside>
  );
}
