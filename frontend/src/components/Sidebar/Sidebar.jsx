import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Icono from "../Icono";
import { useAviso } from "../Aviso/Aviso";
import { useSesion } from "../../features/auth/Sesion.jsx";
import { usaMock } from "../../api/config.js";
import { reiniciarDatos } from "../../api/mock/db.js";
import "./Sidebar.css";

// Secciones del menú, en orden. La ruta de cada una la aporta su feature
// (src/features/<id>/modulo.js); si esa feature todavía no está en el
// proyecto, el botón muestra el aviso "en desarrollo".
// "soloAdmin": solo la ven los usuarios con acceso global (es_global).
const SECCIONES = [
  { id: "dashboard", texto: "Dashboard", icono: "home" },
  { id: "inventario", texto: "Inventario", icono: "box" },
  { id: "ventas", texto: "Ventas y pedidos", icono: "cart" },
  { id: "compras", texto: "Compras", icono: "bag" },
  { id: "clientes", texto: "Clientes", icono: "users" },
  { id: "proveedores", texto: "Proveedores", icono: "truck" },
  { id: "reportes", texto: "Reportes", icono: "chart" },
  { id: "historial", texto: "Historial", icono: "clock" },
  { id: "auditoria", texto: "Auditoría", icono: "shield", soloAdmin: true },
  { id: "usuarios", texto: "Usuarios", icono: "key", soloAdmin: true },
];

const modulos = import.meta.glob("../../features/*/modulo.js", { eager: true, import: "default" });
const RUTA_DE = Object.fromEntries(Object.values(modulos).map((m) => [m.id, m.ruta]));
const ENLACES = SECCIONES.map((s) => ({ ...s, ruta: RUTA_DE[s.id] ?? null }));

// El botón para volver a los datos de ejemplo solo aparece mientras haya
// módulos simulados (VITE_API_MOCK=true).
const HAY_DATOS_SIMULADOS = ENLACES.some((e) => usaMock(e.id));

// "activa" es el id de la sección que debe verse resaltada.
function Sidebar({ activa }) {
  const { mostrar } = useAviso();
  const { sesion, cerrarSesion } = useSesion();
  const usuario = sesion?.usuario ?? {};
  // En celular el menú se pliega bajo una barra superior con botón.
  const [abierto, setAbierto] = useState(false);

  const enlaces = ENLACES.filter((e) => !e.soloAdmin || usuario.esGlobal);

  // Escape cierra el menú desplegado
  useEffect(() => {
    if (!abierto) return;
    const alPresionar = (e) => e.key === "Escape" && setAbierto(false);
    document.addEventListener("keydown", alPresionar);
    return () => document.removeEventListener("keydown", alPresionar);
  }, [abierto]);

  return (
    <aside className={`sb-contenedor${abierto ? " abierto" : ""}`}>
      <nav className="sb" aria-label="Navegación principal">
        <div className="sb-arriba">
          <button type="button" className="sb-boton sb-menu" onClick={() => setAbierto((a) => !a)}
            aria-expanded={abierto} aria-controls="sb-cuerpo"
            aria-label={abierto ? "Cerrar menú" : "Abrir menú"}>
            <Icono nombre={abierto ? "cerrar" : "menu"} />
          </button>
        </div>

        <div className="sb-cuerpo" id="sb-cuerpo">
          <ul className="sb-lista">
            {enlaces.map((e) => {
              const clase = `sb-link${e.id === activa ? " is-active" : ""}`;
              const contenido = (
                <>
                  <Icono nombre={e.icono} />
                  <span>{e.texto}</span>
                  {e.badge && <span className="sb-badge">{e.badge}</span>}
                </>
              );

              return (
                <li key={e.id}>
                  {e.ruta ? (
                    <Link to={e.ruta} className={clase} onClick={() => setAbierto(false)}
                      aria-current={e.id === activa ? "page" : undefined}>
                      {contenido}
                    </Link>
                  ) : (
                    <button type="button" className={clase} onClick={() => mostrar()}>
                      {contenido}
                    </button>
                  )}
                </li>
              );
            })}
          </ul>

          {/* Usuario con sesión iniciada (viene del login) */}
          <div className="sb-usuario">
            <div className="sb-usuario-datos">
              {usuario.nombre && <strong>{usuario.nombre}</strong>}
              <span>{usuario.correo || usuario.usuario}</span>
            </div>
            {HAY_DATOS_SIMULADOS && (
              <button type="button" className="sb-boton" onClick={reiniciarDatos}
                aria-label="Restablecer datos de ejemplo" title="Restablecer datos de ejemplo">
                <Icono nombre="reiniciar" />
              </button>
            )}
            <button type="button" className="sb-boton" onClick={cerrarSesion}
              aria-label="Cerrar sesión" title="Cerrar sesión">
              <Icono nombre="logout" />
            </button>
          </div>
        </div>
      </nav>
    </aside>
  );
}

export default Sidebar;
