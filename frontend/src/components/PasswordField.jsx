import { useState } from "react";
import { TextField } from "./TextField";
import iconoCandado from "../assets/icons/lock.svg";
import iconoOjo from "../assets/icons/eye.svg";
import iconoOjoTachado from "../assets/icons/eye-off.svg";

/** Campo de contraseña con botón para mostrar u ocultar lo escrito. */
export function PasswordField(props) {
  const [visible, setVisible] = useState(false);

  return (
    <TextField
      icon={iconoCandado}
      type={visible ? "text" : "password"}
      trailing={
        <button
          type="button"
          aria-label={visible ? "Ocultar contraseña" : "Mostrar contraseña"}
          aria-pressed={visible}
          onClick={() => setVisible((v) => !v)}
          // El botón mide 24px, pero en pantallas táctiles su área llega a 44x44px.
          className="relative grid size-6 flex-none cursor-pointer place-items-center rounded-campo hover:bg-fondo pointer-coarse:before:absolute pointer-coarse:before:-inset-2.5"
        >
          <img src={visible ? iconoOjoTachado : iconoOjo} alt="" width="16" height="16" />
        </button>
      }
      {...props}
    />
  );
}
