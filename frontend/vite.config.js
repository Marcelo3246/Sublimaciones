import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Vite no carga el .env en process.env al leer este archivo: hay que pedirlo.
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [react(), tailwindcss()],
    server: {
      port: 5173,
      // En desarrollo, la SPA llama a la API por el mismo origen y Vite
      // reenvía /api al backend Django. Así no hay problemas de CORS ni
      // URLs hardcodeadas en el código.
      proxy: {
        "/api": {
          target: env.VITE_PROXY_TARGET || "http://127.0.0.1:8000",
          changeOrigin: true,
        },
      },
    },
  };
});

