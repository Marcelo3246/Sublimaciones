import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { TextField } from "../../../components/TextField";
import { PasswordField } from "../../../components/PasswordField";
import { Button } from "../../../components/Button";
import { FormMessage } from "../../../components/FormMessage";
import iconoUsuario from "../../../assets/icons/user.svg";
import { ErrorAuth } from "../../../services/auth";
import { useLogin } from "../hooks/useLogin";

const esquemaLogin = z.object({
  nombre_usuario: z.string().trim().min(1, "Escribe tu usuario."),
  password: z.string().min(1, "Escribe tu contraseña."),
});

export function LoginForm({ onIngresar }) {
  const [mensaje, setMensaje] = useState(null);
  const login = useLogin();
  const {
    register,
    handleSubmit,
    resetField,
    setFocus,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(esquemaLogin),
    defaultValues: { nombre_usuario: "", password: "" },
  });

  function enviar(datos) {
    setMensaje(null);
    login.mutate(datos, {
      onSuccess: onIngresar,
      onError: (error) => {
        const texto = error instanceof ErrorAuth ? error.message : "Ocurrió un error inesperado. Intenta de nuevo.";
        setMensaje({ tono: "error", texto });
        resetField("password");
        setFocus("password");
      },
    });
  }

  return (
    <form className="flex flex-col gap-5" onSubmit={handleSubmit(enviar)} noValidate>
      <TextField
        label="Usuario"
        icon={iconoUsuario}
        type="text"
        autoComplete="username"
        autoCapitalize="none"
        spellCheck={false}
        placeholder="Tu nombre de usuario"
        error={errors.nombre_usuario?.message}
        autoFocus
        {...register("nombre_usuario")}
      />

      <PasswordField
        label="Contraseña"
        autoComplete="current-password"
        error={errors.password?.message}
        labelAside={
          <button
            type="button"
            className="cursor-pointer text-xs leading-4 font-medium text-marca hover:underline"
            onClick={() => setMensaje({ tono: "info", texto: "Pide al administrador que restablezca tu contraseña." })}
          >
            ¿La olvidaste?
          </button>
        }
        {...register("password")}
      />

      {mensaje && <FormMessage tono={mensaje.tono}>{mensaje.texto}</FormMessage>}

      <Button type="submit" loading={login.isPending} loadingText="Ingresando…">
        Ingresar
      </Button>
    </form>
  );
}
