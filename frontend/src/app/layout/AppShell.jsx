import { Outlet } from "react-router-dom";
import { Aviso } from "../../components/Aviso";
import { Sidebar } from "./Sidebar";

/** Estructura de las páginas internas: menú lateral + contenido de la ruta. */
export function AppShell() {
  return (
    <div className="flex min-h-full max-[860px]:flex-col">
      <Sidebar />
      <main className="min-w-0 flex-1 px-10 pt-7 pb-12 max-[860px]:px-4 max-[860px]:pt-5 max-[860px]:pb-10">
        <Outlet />
      </main>
      <Aviso />
    </div>
  );
}

/** Título de la página (h1) con acciones opcionales a la derecha. */
export function CabeceraPagina({ titulo, children }) {
  return (
    <header className="mb-6 flex flex-wrap items-center justify-between gap-4">
      <title>{`${titulo} · DLL Sublimados`}</title>
      <h1 className="text-[28px] leading-9 font-semibold tracking-[-0.01em]">{titulo}</h1>
      {children && <div className="flex flex-wrap gap-3">{children}</div>}
    </header>
  );
}
