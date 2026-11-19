// Íconos dibujados con trazos SVG, para no depender de librerías externas.
const TRAZOS = {
  home: <><path d="M3 11l9-8 9 8" /><path d="M5 10v10h14V10" /></>,
  box: <><path d="M21 8l-9-5-9 5v8l9 5 9-5z" /><path d="M3 8l9 5 9-5M12 13v8" /></>,
  cart: <><circle cx="9" cy="20" r="1.5" /><circle cx="18" cy="20" r="1.5" /><path d="M2 3h3l2.5 12H19l2-8H6" /></>,
  bag: <><path d="M5 8h14l-1 12H6z" /><path d="M9 8a3 3 0 016 0" /></>,
  users: <><circle cx="9" cy="8" r="3.5" /><path d="M2.5 20c0-3.5 3-6 6.5-6s6.5 2.5 6.5 6" /><path d="M16 4.5a3.5 3.5 0 010 7M18 14c2.5.7 4 2.8 4 6" /></>,
  truck: <><path d="M2 6h11v10H2zM13 9h5l3 3v4h-8" /><circle cx="6.5" cy="18" r="1.8" /><circle cx="17" cy="18" r="1.8" /></>,
  chart: <path d="M6 20V12M12 20V5M18 20v-5" />,
  clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
  shield: <path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" />,
  key: <><circle cx="8" cy="15" r="4" /><path d="M11 12l9-9M17 6l3 3M15 8l2 2" /></>,
  menu: <path d="M4 6h16M4 12h16M4 18h16" />,
  cerrar: <path d="M6 6l12 12M18 6L6 18" />,
  logout: <><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" /><path d="M16 17l5-5-5-5M21 12H9" /></>,
  mas: <path d="M12 5v14M5 12h14" />,
  buscar: <><circle cx="11" cy="11" r="7" /><path d="M20 20l-4-4" /></>,
  editar: <><path d="M4 20h4L19 9l-4-4L4 16z" /><path d="M14 6l4 4" /></>,
  borrar: <><path d="M4 7h16M10 11v6M14 11v6" /><path d="M6 7l1 13h10l1-13M9 7V4h6v3" /></>,
  restaurar: <><path d="M3 12a9 9 0 103-6.7L3 8" /><path d="M3 3v5h5" /></>,
  stock: <><path d="M7 4v16M3 8l4-4 4 4" /><path d="M17 20V4M13 16l4 4 4-4" /></>,
  flecha: <path d="M5 12h14M13 6l6 6-6 6" />,
  atras: <path d="M19 12H5M11 6l-6 6 6 6" />,
  descargar: <><path d="M12 4v11M7 10l5 5 5-5" /><path d="M4 20h16" /></>,
  ojo: <><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" /><circle cx="12" cy="12" r="3" /></>,
  tablero: <><rect x="3" y="4" width="5" height="16" rx="1" /><rect x="10" y="4" width="5" height="10" rx="1" /><rect x="17" y="4" width="4" height="13" rx="1" /></>,
  lista: <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" />,
  check: <path d="M5 12l5 5L20 7" />,
  reiniciar: <><path d="M21 12a9 9 0 11-3-6.7L21 8" /><path d="M21 3v5h-5" /></>,
};

function Icono({ nombre, tamano = 22 }) {
  return (
    <svg viewBox="0 0 24 24" width={tamano} height={tamano} fill="none" stroke="currentColor"
      strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {TRAZOS[nombre]}
    </svg>
  );
}

export default Icono;
