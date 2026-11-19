import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import "./Aviso.css";

const MENSAJE = "Esta sección está en desarrollo y se agregará próximamente.";

const AvisoContext = createContext(null);

// Mensaje flotante abajo al centro ("Cliente guardado", errores, etc.).
// Está en main.jsx, así el aviso sigue visible aunque se cambie de página.
export function AvisoProvider({ children }) {
  const [visible, setVisible] = useState(false);
  const [texto, setTexto] = useState(MENSAJE);
  const [tono, setTono] = useState("normal");
  const temporizador = useRef(null);

  const mostrar = useCallback((mensaje = MENSAJE, opciones = {}) => {
    setTexto(mensaje);
    setTono(opciones.tono ?? "normal");
    setVisible(true);
    clearTimeout(temporizador.current);
    temporizador.current = setTimeout(() => setVisible(false), opciones.duracion ?? 2800);
  }, []);

  // Al cerrar la app se cancela el temporizador pendiente
  useEffect(() => () => clearTimeout(temporizador.current), []);

  const valor = useMemo(() => ({ mostrar }), [mostrar]);

  return (
    <AvisoContext.Provider value={valor}>
      {children}
      <div className={`aviso${visible ? " visible" : ""}${tono === "error" ? " aviso--error" : ""}`}
        role={tono === "error" ? "alert" : "status"}>
        {texto}
      </div>
    </AvisoContext.Provider>
  );
}

// Uso:  const { mostrar } = useAviso();
//       mostrar("Cliente guardado")  |  mostrar("No se pudo guardar", { tono: "error" })
export function useAviso() {
  return useContext(AvisoContext);
}
