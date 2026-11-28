import axios from "axios";
import { useAuth } from "../hooks/useAuth";

/**
 * Cliente HTTP único para la API de Django.
 *
 * - Agrega el JWT de la sesión (Authorization: Bearer ...).
 * - Si la API responde 401, pide un access nuevo con el refresh y repite la
 *   llamada una vez. Si tampoco se puede, cierra la sesión (el router manda
 *   al login).
 *
 * En desarrollo VITE_API_URL es /api/v1 y Vite reenvía /api al backend
 * (ver vite.config.js), así no hay problemas de CORS.
 */
export const API_URL = (import.meta.env.VITE_API_URL || "/api/v1").replace(/\/$/, "");

const RUTA_REFRESH = "/auth/token/refresh/";

export const http = axios.create({
  baseURL: API_URL,
  headers: { Accept: "application/json" },
});

http.interceptors.request.use((config) => {
  const { access } = useAuth.getState();
  if (access && !config.headers.Authorization) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

let refrescando = null;

/** Pide un access nuevo. Si varias llamadas reciben 401 a la vez, se hace un solo refresh. */
function refrescarToken() {
  const { refresh } = useAuth.getState();
  if (!refresh) return Promise.resolve(false);

  refrescando ??= axios
    .post(`${API_URL}${RUTA_REFRESH}`, { refresh })
    .then(({ data }) => {
      useAuth.getState().actualizarTokens(data);
      return true;
    })
    .catch(() => false)
    .finally(() => {
      refrescando = null;
    });

  return refrescando;
}

http.interceptors.response.use(
  (respuesta) => respuesta,
  async (error) => {
    const original = error.config;
    // `sinSesion`: llamadas que no usan la sesión guardada (p. ej. el login).
    if (error.response?.status === 401 && original && !original.sinSesion && !original._reintento) {
      original._reintento = true;
      if (await refrescarToken()) {
        original.headers.Authorization = `Bearer ${useAuth.getState().access}`;
        return http(original);
      }
      useAuth.getState().limpiarSesion();
    }
    return Promise.reject(error);
  }
);
