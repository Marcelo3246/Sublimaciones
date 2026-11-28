import { create } from "zustand";

/**
 * Mensaje flotante abajo al centro (components/Aviso.jsx).
 *   const mostrar = useAviso((s) => s.mostrar);
 *   mostrar("Pedido guardado");
 */
let temporizador;

export const useAviso = create((set) => ({
  texto: "",
  visible: false,

  mostrar: (texto, duracion = 2800) => {
    clearTimeout(temporizador);
    set({ texto, visible: true });
    temporizador = setTimeout(() => set({ visible: false }), duracion);
  },
}));
