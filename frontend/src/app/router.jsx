import { Navigate, Route, Routes } from "react-router-dom";
import { LoginPage } from "../features/auth/pages/LoginPage";
import { RutaProtegida } from "../features/auth/components/RutaProtegida";
import { DashboardPage } from "../features/reportes/pages/DashboardPage";
import { AppShell } from "./layout/AppShell";

/** Rutas de la SPA. Todo lo que va dentro de <RutaProtegida> exige sesión. */
export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<RutaProtegida />}>
        <Route element={<AppShell />}>
          <Route path="/" element={<DashboardPage />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
