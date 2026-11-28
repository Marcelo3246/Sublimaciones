import { useQuery } from "@tanstack/react-query";
import { obtenerDashboard } from "../api/reportesApi";

/** Datos del dashboard; se refrescan solos cada minuto mientras la pantalla está abierta. */
export function useDashboard() {
  return useQuery({
    queryKey: ["reportes", "dashboard"],
    queryFn: obtenerDashboard,
    refetchInterval: 60_000,
  });
}
