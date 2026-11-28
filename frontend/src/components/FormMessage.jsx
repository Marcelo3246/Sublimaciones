const TONOS = {
  error: "bg-peligro-fondo text-peligro",
  info: "bg-fondo text-texto-secundario",
};

/** Mensaje general del formulario (error del servidor, aviso). */
export function FormMessage({ tono = "info", children }) {
  return (
    <p
      role={tono === "error" ? "alert" : "status"}
      className={`rounded-campo px-3 py-2 text-[13px] leading-[18px] ${TONOS[tono] ?? TONOS.info}`}
    >
      {children}
    </p>
  );
}
