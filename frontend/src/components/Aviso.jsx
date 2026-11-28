import { useAviso } from "../hooks/useAviso";

/** Muestra el mensaje de useAviso. Va una sola vez, en el AppShell. */
export function Aviso() {
  const { texto, visible } = useAviso();

  return (
    <div
      role="status"
      className={`pointer-events-none fixed bottom-6 left-1/2 z-50 max-w-[calc(100vw-32px)] -translate-x-1/2 rounded-campo bg-texto px-4 py-2.5 text-white shadow-tarjeta transition-[opacity,translate] duration-200 motion-reduce:transition-none ${
        visible ? "translate-y-0 opacity-100" : "translate-y-2 opacity-0"
      }`}
    >
      {texto}
    </div>
  );
}
