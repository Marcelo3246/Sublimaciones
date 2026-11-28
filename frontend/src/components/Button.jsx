const VARIANTES = {
  primary: {
    boton: "border-transparent bg-marca text-white hover:enabled:bg-marca-hover active:enabled:bg-marca-activo",
    spinner: "border-white/40 border-t-white",
  },
  secondary: {
    boton: "border-borde-fuerte bg-superficie text-texto hover:enabled:bg-fondo active:enabled:bg-borde",
    spinner: "border-borde border-t-marca",
  },
};

/**
 * Botón del sistema. `variant`: "primary" (morado) o "secondary" (blanco con borde).
 * `inline`: ancho según el texto en vez de ocupar toda la fila.
 * Con `loading` muestra un indicador y bloquea nuevos clics.
 */
export function Button({
  variant = "primary",
  inline = false,
  loading = false,
  loadingText,
  className = "",
  disabled,
  children,
  ...props
}) {
  const estilo = VARIANTES[variant] ?? VARIANTES.primary;

  return (
    <button
      disabled={loading || disabled}
      aria-busy={loading || undefined}
      className={`relative inline-flex h-9 cursor-pointer items-center justify-center gap-2 rounded-campo border px-4 text-sm font-medium whitespace-nowrap transition-colors duration-120 disabled:cursor-default aria-busy:opacity-85 disabled:not-aria-busy:opacity-50 pointer-coarse:after:absolute pointer-coarse:after:inset-x-0 pointer-coarse:after:-inset-y-1 ${
        inline ? "w-auto" : "w-full"
      } ${estilo.boton} ${className}`}
      {...props}
    >
      {loading && (
        <span
          aria-hidden="true"
          className={`size-3.5 animate-spin rounded-full border-2 motion-reduce:[animation-duration:2s] ${estilo.spinner}`}
        />
      )}
      {loading && loadingText ? loadingText : children}
    </button>
  );
}
