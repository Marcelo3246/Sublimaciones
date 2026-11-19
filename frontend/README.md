# Sublimación — Frontend

Interfaz web del sistema de gestión del negocio de sublimación (React + Vite).
Funciona sola con datos de ejemplo mientras el backend Django
([Marcelo3246/Sublimaciones](https://github.com/Marcelo3246/Sublimaciones)) termina sus endpoints.

## Cómo correrlo

```bash
npm install
cp .env.example .env     # en PowerShell: Copy-Item .env.example .env
npm run dev              # http://localhost:5173
```

Usuario de prueba (login simulado): `admin` / `admin123` (también acepta `admin@sublimacion.com`).

Los datos de ejemplo se guardan en el navegador. Para volver a los originales, usar el
botón ↻ junto a "Cerrar sesión" (solo aparece en modo simulado).

| Comando           | Qué hace                                  |
| ----------------- | ----------------------------------------- |
| `npm run dev`     | Servidor de desarrollo en el puerto 5173  |
| `npm run build`   | Genera la versión final en `dist/`        |
| `npm run preview` | Sirve `dist/` para probarla               |

## Módulos

| Módulo           | Ruta                          | Qué permite                                                         |
| ---------------- | ----------------------------- | ------------------------------------------------------------------- |
| Login            | `/login`                      | Ingreso con JWT                                                     |
| Dashboard        | `/`                           | Cifras del día y del mes, entregas próximas, stock bajo             |
| Inventario       | `/inventario`                 | Productos, materia prima, categorías y ajustes de stock             |
| Ventas y pedidos | `/ventas`, `/ventas/nueva`    | Tablero por estado (arrastrar y soltar), lista, detalle, nueva venta |
| Compras          | `/compras`, `/compras/nueva`  | Órdenes de compra, confirmar, recibir (suma stock), anular          |
| Clientes         | `/clientes`                   | Alta, edición, búsqueda y desactivación                             |
| Proveedores      | `/proveedores`                | Alta, edición, búsqueda y desactivación                             |
| Reportes         | `/reportes`                   | Totales por período y rankings, exportables a CSV                   |
| Historial        | `/historial`                  | Movimientos de stock con filtros y CSV                              |
| Auditoría        | `/auditoria`                  | Bitácora de acciones con antes/después (solo administradores)       |
| Usuarios         | `/usuarios`                   | Usuarios, roles y contraseñas (solo administradores)                |

## Estructura

```text
src/
├── main.jsx, App.jsx        Arranque y rutas (cada feature registra las suyas)
├── api/                     Conexión con el backend
│   ├── config.js            Variables VITE_* y qué módulos están simulados
│   ├── cliente.js           fetch con JWT, refresh automático y errores de DRF
│   ├── recurso.js           CRUD genérico (listar, crear, actualizar, desactivar)
│   ├── sesion.js            Tokens guardados
│   └── mock/                Base de datos simulada en el navegador
├── components/              Piezas compartidas (Layout, Sidebar, Modal, Campo, Panel…), cada una con su .css
├── hooks/                   useConsulta, useFormulario, useDiferido
├── styles/                  Estilos globales: tokens.css (colores de Figma), base.css y lo que
│                            usan varias features (tablas, formularios, paginas, documentos)
├── utils/                   Formatos de dinero/fechas, validaciones, CSV
└── features/                Un módulo por carpeta
    └── <feature>/
        ├── rutas.jsx        Páginas de la feature (App.jsx las carga solo)
        ├── modulo.js        Habilita su entrada en el menú lateral
        ├── api.js           Endpoints del backend + versión simulada
        ├── semilla.js       Datos de ejemplo
        └── *.jsx / *.css    Pantallas (cada .jsx importa su propio .css)
```

**Estilos:** no hay CSS dentro de los JSX (ni `style={...}`). Cada componente o pantalla
con estilos propios tiene su `.css` al lado con el mismo nombre (`Modal.jsx` → `Modal.css`) y
lo importa. En `styles/` solo queda lo global: colores y tipografía (`tokens.css`), el reset
(`base.css`) y las piezas que comparten varias features sin ser un componente.

Cada feature es independiente: si su carpeta no está, la app compila igual y el menú
muestra "en desarrollo" en esa sección.

## Documentación

- [Conectar con el backend](docs/CONECTAR-BACKEND.md): variables, contrato de cada endpoint y lo que falta pedirle al backend.
