---
status: borrador
type: documento
tags:
  - frontend
  - react
  - estructura
  - especificacion
created: 2026-11-04
version: 0.2
---

# 08 Estructura del frontend

Cómo se organiza la SPA de DLL Sublimados en React + Vite + Tailwind CSS y cómo se mapea a los 11 módulos del backend. Estructura de repositorio general en [04 Arquitectura del monolito modular](04-arquitectura-del-monolito-modular.md); aquí va el detalle del `frontend/`.

## Stack

| Aspecto | Decisión |
| --- | --- |
| Framework | React 19+ con JavaScript |
| Empaquetado | Vite 5+ |
| Estilos | Tailwind CSS (config de tokens: colores por local, tipografía, componentes) |
| Server state | TanStack Query para caché y refetch de datos de la API |
| Estado local | Zustand (sesión: `auth`, `localActivo`, preferencias del usuario) |
| HTTP | Axios con interceptores (inyección de JWT, refresh automático, errores a toasts) |
| Formularios | React Hook Form + Zod (validación de medidas, tallas, montos multi-moneda) |
| PDF/impresión | Window print sobre vista de documento (las plantillas reales generan en `documents` del backend) |

## Árbol de carpetas

```
frontend/
├── vite.config.js               # proxy de /api al Django en dev
├── index.html
└── src/
    ├── main.jsx
    ├── app/
    │   ├── router.jsx           # rutas y guards de sesión y rol
    │   ├── layout/
    │   │   ├── AppShell.jsx     # sidebar + topbar
    │   │   ├── Sidebar.jsx      # nav segun permisos del usuario
    │   │   └── TopBar.jsx       # selector de local (si es global), tipo de cambio, usuario
    │   └── providers/           # AuthProvider, LocalProvider, QueryClient
    ├── services/
    │   ├── http.js              # axios base, interceptores de token
    │   └── auth.js              # login, refresh, logout
    ├── features/                # una carpeta por módulo del backend
    │   ├── auth/                # login, registro, perfil y configuración de usuario
    │   ├── auditoria/           # bitácora de usuarios, bitácora de stock, panel admin
    │   ├── catalogo/            # materiales, productos, servicios, UM y tallas
    │   ├── inventario/          # stock, lotes, transferencias
    │   ├── compras/             # proveedores, órdenes y recepción, comparador
    │   ├── produccion/          # órdenes, tablero de ruta, operaciones de máquina
    │   ├── ventas/              # clientes, pedidos, facturación
    │   ├── precios/             # matriz de precios (consulta y mantenimiento)
    │   ├── rrhh/                # trabajadores: cargo, locales, vinculo con login
    │   ├── documentos/          # generador y repositorio de documentos
    │   └── reportes/            # dashboard y reportes exportables
    ├── components/              # UI compartida
    ├── hooks/                   # useAuth, usePermisos, useLocalActivo, useTiposCambio
    └── styles/
```

Dentro de cada `feature/`, la convención es la misma para los 11 módulos:

```
features/inventario/
├── api/            # endpoints del módulo: funciones tipadas (getStock, crearLote...)
├── pages/          # pantallas: StockView, LotesView, TransferenciasView
├── components/     # componentes propios del módulo (TablaLotes, SelectorMedicion...)
├── hooks/          # queries/mutations del módulo (useLotesQuery, useTransferir)
└── types.ts        # tipos que espejan los modelos en español del backend
```

## Páginas por módulo (mapeo a los RF de [03 Requerimientos del sistema](03-requerimientos-del-sistema.md))

| Feature | Páginas | RF |
| --- | --- | --- |
| `auth` | Login, Registro (SignUp), Perfil y configuración de usuario | RF-01, RF-03 |
| `auditoria` | Bitácora de usuarios, Bitácora de stock, Panel admin con filtros | RF-06–RF-09 |
| `catalogo` | Materiales, Productos (+variantes), Servicios, UM y tallas | RF-10–RF-15 (RF-12 ext) |
| `inventario` | Vista de productos, Vista de materia prima, Transferencias (solicitar/despachar/recibir) | RF-16–RF-24 |
| `compras` | Proveedores, Órdenes de compra, Recepción, Comparador de precios | RF-25–RF-29 |
| `produccion` | Órdenes de producción, Tablero de ruta por paso, Registro de consumo y máquina | RF-30–RF-35 |
| `ventas` | Pedidos abiertos, Ventas (facturadas/entregadas), Factura propia, Nota de entrega | RF-36–RF-43 |
| `precios` | Matriz de consulta (vendedor), Matriz de mantenimiento (admin) | RF-44–RF-47 |
| `rrhh` | Trabajadores (cargo, locales, login) — *nómina diferida* | RF-48 (RF-49–RF-51 diferidos) |
| `documentos` | Generador por tipo de documento, Repositorio con búsqueda | RF-52–RF-55 |
| `reportes` | Dashboard por rol, Reportes exportables | RF-56–RF-58 |

## Componentes UI compartidos (Tailwind)

| Componente | Uso |
| --- | --- |
| `DataTable` | listado paginado y filtrable con estados y acciones en row (stock, pedidos...) |
| `BadgeEstado` | estado de negocio (`en_produccion`, `en_transito`, `dañado`...) con color de paleta por estado |
| `ModalConfirm` | confirmaciones que exigen justificación (anulación de venta, desperdicio) |
| `SelectorMedicion` | cantidad + UM para consumos por medición (metro/metraje/talla) con validación |
| `SelectorLote` | búsqueda de lote por código y muestra de restante, bloquea si es insuficiente |
| `SelectorLocal` | filtro obligatorio; puede cambiar de local únicamente el usuario global |
| `MontoDobleMoneda` | monto en USD/Bs con el tipo de cambio del día |
| `TimelineEstados` | línea de progreso de la máquina de estados del pedido ([05 Flujos de proceso](05-flujos-de-proceso.md#flujo-3--ventas)) |
| `Sidebar` / `AppShell` | navegación por permisos; los módulos se ocultan cuando el usuario no tiene acceso |

## Reglas de comportamiento

1. **El selector del `local` activo** alimenta la consulta de todas las pantallas y se guarda en `LocalProvider`; por defecto el usuario entra al local que tiene asignado.
2. Los estados de los pedidos se muestran como **badges y TimelineEstados**; la SPA solo bloquea botones, el estado real lo controla el backend ([04 Arquitectura del monolito modular](04-arquitectura-del-monolito-modular.md#reglas-de-modularidad-obligatorias-para-el-código)).
3. Toda escritura genera el mensaje de confirmación con detalle de lo que hará (p. ej. "consumir 1.8 m del lote PARR-0123, restante 8.2 m").
4. Nada de lógica de precios en el frontend: el precio lo calcula la API; si se pierde la conexión, se recalcula al reconectar.
5. Responsive desktop + tablet: el piso de producción usa formularios con elementos grandes, en modo táctil.
6. Nomenclatura: componentes `PascalCase`, hooks `useXxx`, servicios de API `moduloApi.ts`, tipos espejan las tablas de [06 Modelo de datos](06-modelo-de-datos.md).
7. TanStack Query mantiene caché e invalidación después de cada mutación, para pantallas rápidas y consistentes.

## Referencias

- [04 Arquitectura del monolito modular](04-arquitectura-del-monolito-modular.md)
- [06 Modelo de datos](06-modelo-de-datos.md)
- [Glosario](referencias/glosario-del-negocio.md)