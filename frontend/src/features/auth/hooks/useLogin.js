import { useMutation } from "@tanstack/react-query";
import { iniciarSesion } from "../../../services/auth";

/** Mutación de login: { nombre_usuario, password } -> sesión guardada. */
export function useLogin() {
  return useMutation({ mutationFn: iniciarSesion });
}
