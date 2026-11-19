import EstadoVacio from "../../components/EstadoVacio.jsx";

// Tabla de "menor stock". Sirve tanto para productos como para materia prima.
// Si no hay filas muestra el mensaje "vacio"; si la cantidad es 0 se pinta en rojo.
function TablaStock({ columna, filas, vacio }) {
  if (filas.length === 0) return <EstadoVacio texto={vacio} />;

  return (
    <table className="tabla">
      <thead>
        <tr><th>{columna}</th><th>Cantidad</th></tr>
      </thead>
      <tbody>
        {filas.map((f) => (
          <tr key={f.id}>
            <td>{f.descripcion}<small>{f.detalle}</small></td>
            <td><span className={`cant${f.cantidad === 0 ? " cero" : ""}`}>{f.cantidad}</span></td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TablaStock;
