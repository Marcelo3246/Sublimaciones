import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// El backend Django tiene CORS abierto para http://localhost:5173,
// así que el servidor de desarrollo se queda en ese puerto.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: true },
})
