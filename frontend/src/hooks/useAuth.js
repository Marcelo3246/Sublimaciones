import { create } from "zustand";
import { persist } from "zustand/middleware";

/**
 * Sesión del usuario (Zustand). Se guarda en localStorage para no perderla
 * al recargar la página.
 *
 * `usuario` tiene la misma forma que GET /api/v1/core/perfil/
 * (UsuarioSerializer): id, nombre_usuario, correo, nombre, apellido, rol,
 * local, local_info, es_global, activo.
 */
export const useAuth = create(
  persist(
    (set) => ({
      access: null,
      refresh: null,
      usuario: null,

      guardarSesion: ({ access, refresh, usuario }) => set({ access, refresh, usuario }),

      // SimpleJWT rota el refresh (ROTATE_REFRESH_TOKENS): si viene uno nuevo, se reemplaza.
      actualizarTokens: ({ access, refresh }) =>
        set((estado) => ({ access, refresh: refresh ?? estado.refresh })),

      limpiarSesion: () => set({ access: null, refresh: null, usuario: null }),
    }),
    {
      name: "dll-sublimados.sesion",
      partialize: ({ access, refresh, usuario }) => ({ access, refresh, usuario }),
    }
  )
);
