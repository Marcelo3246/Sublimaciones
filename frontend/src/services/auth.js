import { http } from "./http";
import { useAuth } from "../hooks/useAuth";

/**
 * Autenticación contra el backend (SimpleJWT), según backend/config/urls.py
 * y backend/apps/core/urls.py:
 *   POST /api/v1/auth/token/          { nombre_usuario, password } -> { access, refresh }
 *   POST /api/v1/auth/token/refresh/  { refresh } -> { access, refresh }   (services/http.js)
 *   GET  /api/v1/core/perfil/         -> datos del usuario (UsuarioSerializer)
 *
 * El backend todavía no tiene ruta de logout (falta la app token_blacklist):
 * cerrar sesión solo borra los tokens del navegador.
 *
 * Con VITE_AUTH_MOCK=true el login se simula en el navegador con USUARIO_DEMO,
 * para trabajar sin el backend levantado.
 */
const USA_MOCK = import.meta.env.VITE_AUTH_MOCK === "true";

const RUTAS = {
  token: "/auth/token/",
  perfil: "/core/perfil/",
};

export const USUARIO_DEMO = { nombre_usuario: "admin", password: "admin123" };

/** Error con un mensaje listo para mostrar en el formulario. */
export class ErrorAuth extends Error {}

const esperar = (ms) => new Promise((resolver) => setTimeout(resolver, ms));

async function loginSimulado({ nombre_usuario, password }) {
  await esperar(700);
  if (nombre_usuario.toLowerCase() !== USUARIO_DEMO.nombre_usuario || password !== USUARIO_DEMO.password) {
    throw new ErrorAuth("Usuario o contraseña incorrectos.");
  }
  return {
    access: "mock-access",
    refresh: "mock-refresh",
    usuario: {
      id: 1,
      nombre_usuario: "admin",
      correo: "admin@sublimacion.com",
      nombre: "Administrador",
      apellido: "",
      rol: "admin",
      local: null,
      local_info: null,
      es_global: true,
      activo: true,
    },
  };
}

async function loginReal({ nombre_usuario, password }) {
  let tokens;
  try {
    // SimpleJWT espera el USERNAME_FIELD de core.Usuario: "nombre_usuario".
    const { data } = await http.post(RUTAS.token, { nombre_usuario, password }, { sinSesion: true });
    tokens = data;
  } catch (error) {
    const status = error.response?.status;
    if (status === 400 || status === 401) throw new ErrorAuth("Usuario o contraseña incorrectos.");
    if (!error.response) throw new ErrorAuth("No se pudo conectar con el servidor.");
    throw new ErrorAuth("El servidor no respondió como se esperaba. Intenta de nuevo.");
  }

  // Si el perfil falla, se entra igual con el nombre de usuario escrito.
  let usuario = { nombre_usuario };
  try {
    const { data } = await http.get(RUTAS.perfil, {
      headers: { Authorization: `Bearer ${tokens.access}` },
      sinSesion: true,
    });
    usuario = data;
  } catch {
    /* sin datos del perfil */
  }

  return { access: tokens.access, refresh: tokens.refresh, usuario };
}

/** Inicia sesión y la guarda. Devuelve { access, refresh, usuario }. */
export async function iniciarSesion(credenciales) {
  const sesion = USA_MOCK ? await loginSimulado(credenciales) : await loginReal(credenciales);
  useAuth.getState().guardarSesion(sesion);
  return sesion;
}

export function cerrarSesion() {
  useAuth.getState().limpiarSesion();
}
