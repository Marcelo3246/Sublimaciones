import './EstadoVacio.css'

// Mensaje que se muestra cuando una sección todavía no tiene información.
function EstadoVacio({ texto }) {
  return <p className="vacio">{texto}</p>;
}

export default EstadoVacio;
