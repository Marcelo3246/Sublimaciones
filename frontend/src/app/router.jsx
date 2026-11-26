import { Navigate, Route, Routes } from "react-router-dom";
import { LoginPage } from "../features/auth/pages/LoginPage";
import { RutaProtegida } from "../features/auth/components/RutaProtegida";
import { InicioProvisional } from "./InicioProvisional";

/** Rutas de la SPA. Todo lo que va dentro de <RutaProtegida> exige sesión. */
export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<RutaProtegida />}>
        <Route path="/" element={<InicioProvisional />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
