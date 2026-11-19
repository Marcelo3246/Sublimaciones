import { Link } from "react-router-dom";
import "./Panel.css";

// Caja blanca con título y un enlace arriba a la derecha. Se reutiliza
// en todas las secciones; el contenido va en "children".
// El enlace puede ir a una ruta ("a") o ejecutar una función ("onEnlace").
function Panel({ titulo, enlace, a, onEnlace, extra, className = "", children }) {
  return (
    <article className={`panel ${className}`}>
      {(titulo || enlace || extra) && (
        <div className="panel-cab">
          <h2>{titulo}</h2>
          {extra}
          {enlace && a && <Link to={a} className="enlace">{enlace}</Link>}
          {enlace && !a && <button type="button" className="enlace" onClick={onEnlace}>{enlace}</button>}
        </div>
      )}
      {children}
    </article>
  );
}

export default Panel;
