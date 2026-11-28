import { useId } from "react";

/**
 * Campo de texto con ícono a la izquierda, acción opcional a la derecha
 * (p. ej. mostrar contraseña) y mensaje de error accesible.
 * Funciona con register() de React Hook Form (en React 19 `ref` llega como prop).
 */
export function TextField({ label, icon, error, labelAside, trailing, className = "", ref, ...inputProps }) {
  const id = useId();
  const idError = `${id}-error`;

  return (
    <div className={`flex w-full flex-col gap-2 ${className}`}>
      <div className="flex min-h-4 items-center justify-between">
        <label htmlFor={id} className="text-xs leading-4 font-medium tracking-[0.1px]">
          {label}
        </label>
        {labelAside}
      </div>

      <div
        className={`flex h-9 items-center gap-2 rounded-campo border bg-superficie pr-1.5 pl-3 transition-[border-color,box-shadow] duration-120 ${
          error
            ? "border-peligro ring-1 ring-peligro"
            : "border-borde-fuerte focus-within:border-marca-foco focus-within:ring-1 focus-within:ring-marca-foco"
        }`}
      >
        {icon && <img src={icon} alt="" width="16" height="16" className="block flex-none" />}
        <input
          ref={ref}
          id={id}
          aria-invalid={error ? "true" : undefined}
          aria-describedby={error ? idError : undefined}
          // En pantallas táctiles: 16px evita el zoom de iOS y el área táctil llega a 44px.
          className="h-full min-w-0 flex-1 bg-transparent text-sm outline-none placeholder:text-borde-fuerte pointer-coarse:-my-1 pointer-coarse:h-11 pointer-coarse:text-base"
          {...inputProps}
        />
        {trailing}
      </div>

      {error && (
        <p id={idError} className="text-xs leading-4 text-peligro">
          {error}
        </p>
      )}
    </div>
  );
}
