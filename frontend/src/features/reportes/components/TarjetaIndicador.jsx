/** Cifra destacada del dashboard. Con `alerta` el valor se pinta en ámbar. */
export function TarjetaIndicador({ titulo, valor, nota, alerta = false }) {
  return (
    <article className="rounded-tarjeta border border-borde bg-superficie px-6 py-5 shadow-tarjeta">
      <h2 className="text-[13px] font-medium text-texto-secundario">{titulo}</h2>
      <p
        className={`mt-2 mb-1 text-[28px] leading-9 font-semibold tracking-[-0.02em] tabular-nums ${
          alerta ? "text-alerta" : ""
        }`}
      >
        {valor}
      </p>
      <p className="text-[13px] text-texto-secundario">{nota}</p>
    </article>
  );
}
