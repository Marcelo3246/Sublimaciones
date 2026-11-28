/** Caja blanca con título. El contenido va en `children`; `extra` queda a la derecha del título. */
export function Panel({ titulo, extra, className = "", children }) {
  return (
    <section
      aria-label={titulo}
      className={`overflow-hidden rounded-tarjeta border border-borde bg-superficie shadow-tarjeta ${className}`}
    >
      <header className="flex items-center justify-between gap-3 border-b border-borde px-6 py-4 max-[860px]:px-4">
        <h2 className="text-base font-semibold">{titulo}</h2>
        {extra}
      </header>
      {children}
    </section>
  );
}

/** Mensaje para cuando una sección todavía no tiene información. */
export function EstadoVacio({ children }) {
  return <p className="px-6 py-9 text-center text-texto-secundario">{children}</p>;
}
