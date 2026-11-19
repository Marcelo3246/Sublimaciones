# Conectar el frontend con el backend Django

Hoy cada módulo responde con datos simulados en el navegador. Todas las llamadas
pasan por `src/api/` y por el `api.js` de cada feature, así que conectar el backend
**no requiere tocar las pantallas**: se cambia una variable y, si algún nombre de
campo no coincide, se ajusta solo el `api.js` de esa feature.

Los nombres de campos y estados ya son los de los modelos del repo oficial
(`sales.PedidoVenta`, `purchasing.OrdenCompra`, `catalog.Material`, etc.).

> **Aviso (19/11/2026):** el PR #3 del repo oficial (abierto, sin aceptar) reorganiza el
> backend en `backend/apps/`. El login y el perfil (sección 3) ya siguen ese PR.
> El contrato por módulo (sección 5) todavía sigue los modelos de `develop`: en el PR #3,
> `sales` y `purchasing` quedan sin modelos (los define el Grupo de Base de Datos) y
> `catalog`, `inventory` y `audit` cambian (`Stock`, `Lote`, `BitacoraAccion`…). Cuando el
> PR se acepte y esos modelos estén listos, hay que revisar la sección 5.

---

## 1. Variables de entorno (`.env`)

| Variable          | Valor de ejemplo                 | Para qué sirve                                                                 |
| ----------------- | -------------------------------- | ------------------------------------------------------------------------------ |
| `VITE_API_URL`    | `http://localhost:8000/api/v1`   | URL base de la API                                                             |
| `VITE_AUTH_MOCK`  | `true` / `false`                 | Login simulado o real                                                          |
| `VITE_API_MOCK`   | `true` / `false`                 | Datos simulados o reales en **todos** los módulos                              |
| `VITE_API_REALES` | `clientes,proveedores`           | Módulos que ya usan el backend aunque `VITE_API_MOCK` siga en `true`           |
| `VITE_LOCAL_ID`   | `1`                              | Local que se envía al crear ventas/compras si el token no trae uno             |

Nombres válidos para `VITE_API_REALES`: `dashboard`, `inventario`, `ventas`, `compras`,
`clientes`, `proveedores`, `reportes`, `historial`, `auditoria`, `usuarios`.

Después de cambiar el `.env` hay que reiniciar `npm run dev`.

---

## 2. Paso a paso para conectar un módulo

1. El backend publica el endpoint (ver la sección 5 para saber cuál espera cada módulo).
2. Levantar Django (`python manage.py runserver` desde la raíz del repo; antes del PR #3 era
   `python src/manage.py runserver`) y el frontend (`npm run dev`).
3. Activar solo ese módulo: `VITE_API_REALES=clientes` y reiniciar `npm run dev`.
4. Probar la pantalla. Si algo no se ve, abrir las herramientas del navegador (F12 → Red)
   y comparar la respuesta con lo que lee la pantalla.
5. Si el serializer usa otros nombres, adaptarlos en el `api.js` de la feature con
   `desdeApi` / `haciaApi` (ejemplo abajo). Las pantallas no se tocan.
6. Repetir con el siguiente módulo. Cuando todos estén conectados:
   `VITE_AUTH_MOCK=false`, `VITE_API_MOCK=false` y `VITE_API_REALES=` vacío.

Ejemplo de adaptación, si el backend devolviera `razon_social` en vez de `nombre`:

```js
// src/features/clientes/api.js
export const clientesApi = crearRecurso({
  modulo: 'clientes',
  endpoint: '/sales/clientes/',
  // ...
  desdeApi: ({ razon_social, ...resto }) => ({ ...resto, nombre: razon_social }),
  haciaApi: ({ nombre, ...resto }) => ({ ...resto, razon_social: nombre }),
})
```

---

## 3. Login y sesión (SimpleJWT)

El frontend ya hace todo esto (`src/features/auth/api.js` y `src/api/cliente.js`). Las rutas
están juntas en `RUTAS_AUTH` (`src/api/config.js`) y siguen el PR #3 del repo oficial:

| Acción         | Llamada                                                    | Respuesta esperada               |
| -------------- | ---------------------------------------------------------- | -------------------------------- |
| Ingresar       | `POST /auth/token/` `{ nombre_usuario, password }`         | `{ access, refresh }`            |
| Datos del menú | `GET /core/perfil/` (con token)                            | `UsuarioSerializer`: `id, nombre_usuario, correo, nombre, apellido, rol, local, es_global` |
| Renovar token  | `POST /auth/token/refresh/` `{ refresh }`                  | `{ access, refresh }`            |
| Salir          | — (solo se borran los tokens del navegador)                | —                                |

- Cada llamada lleva `Authorization: Bearer <access>`.
- Si una llamada devuelve **401**, el frontend pide un token nuevo con el refresh y la
  repite una vez. Si el refresh también falla, vuelve al login.
- El formulario pide **Usuario**, que se envía como `nombre_usuario` (el `USERNAME_FIELD`
  de `core.Usuario`).
- De `/core/perfil/` se toman el nombre que se muestra en el menú, `es_global` (muestra
  Auditoría y Usuarios) y `local` (el local con el que se crean ventas, compras y
  movimientos). Si `/core/perfil/` falla, se entra igual, pero sin permisos de administrador.

Lo que falta en el backend del PR #3:

- **Logout real:** `settings.py` tiene `ROTATE_REFRESH_TOKENS` y `BLACKLIST_AFTER_ROTATION`,
  pero no instala `"rest_framework_simplejwt.token_blacklist"`. Sin esa app, el refresh viejo
  sigue sirviendo hasta que vence (7 días). Para invalidarlo hay que agregar la app a
  `INSTALLED_APPS`, correr `migrate` y publicar
  `path("api/v1/auth/token/blacklist/", TokenBlacklistView.as_view())`. Después se agrega
  `logout` a `RUTAS_AUTH` y se llama desde `logout()` en `src/features/auth/api.js`.
- CORS ya permite `http://localhost:5173`.

---

## 4. Lo que el frontend asume de DRF

Ya coincide con el `REST_FRAMEWORK` de `settings.py`:

- **Rutas** con barra final (`/sales/clientes/`, `/sales/clientes/5/`), como genera un `DefaultRouter`.
- **Paginación** `PageNumberPagination`: el frontend sigue los enlaces `next` y junta todas las páginas.
  También acepta una lista simple sin paginar.
- **Búsqueda** con `?search=` (`SearchFilter`). Cada `api.js` indica en qué campos busca.
- **Filtros exactos** con `?campo=valor` (`DjangoFilterBackend` + `filterset_fields`): `estado`, `categoria`, `tipo_item`…
- **Activos**: los listados piden `?activo=true`. Agregar `activo` a `filterset_fields`.
- **Fechas**: Historial y Auditoría envían `?desde=YYYY-MM-DD&hasta=YYYY-MM-DD` (ver el ejemplo de la sección 6).
- **DELETE = borrado lógico**: el frontend llama a `DELETE` para "Desactivar"; el ViewSet debe
  poner `activo = False` (modelo `Auditable`) en vez de borrar. Para reactivar envía `PATCH { activo: true }`.
- **Errores**: `{ "detail": "..." }` se muestra como mensaje general y `{ "campo": ["..."] }`
  aparece debajo del campo correspondiente del formulario.
- **Decimales** pueden venir como texto (`"12.50"`); el frontend los convierte.

---

## 5. Contrato por módulo

Para cada módulo: el endpoint, los campos que lee la pantalla y lo que envía.
Lo marcado con ⚠️ **no existe todavía en los modelos** y hay que pedirlo al backend
(o adaptarlo en el `api.js`).

### Clientes — `src/features/clientes/api.js`

`/sales/clientes/` (CRUD) · búsqueda en `nombre`, `rif`, `telefono`, `correo`

Lee y envía: `id, nombre, rif, telefono, correo, activo`.

### Proveedores — `src/features/proveedores/api.js`

`/purchasing/proveedores/` (CRUD) · búsqueda en `nombre`, `persona_contacto`, `rif`, `telefono`

Lee y envía: `id, nombre, persona_contacto, telefono, rif, moneda_predeterminada ("USD"|"BS"), activo`.

### Inventario — `src/features/inventario/api.js`

| Endpoint                     | Uso                                        | Filtros            |
| ---------------------------- | ------------------------------------------ | ------------------ |
| `/catalog/categorias/`       | CRUD `{ nombre, tipo }`                    | `activo`           |
| `/catalog/unidades-medida/`  | Solo lectura `{ id, codigo, nombre, tipo }`| —                  |
| `/catalog/productos/`        | CRUD                                       | `categoria`, `search` |
| `/catalog/materiales/`       | CRUD                                       | `categoria`, `search` |
| `/inventory/movimientos/`    | `GET` listado, `POST` ajuste manual        | ver Historial      |

Producto: `id, nombre, categoria, tipo, activo` y además, de solo lectura:
- ⚠️ `precio_base`, `moneda`: precio vigente de `pricing.ItemMatrizPrecios`. Al crear/editar el
  frontend envía `precio_base`; el backend debe guardarlo en la matriz de precios.
- ⚠️ `cantidad_disponible`, `um`: suma de `inventory.Existencia` del local.

Materia prima: `id, nombre, categoria, formato_stock, tipo_medicion, um_predeterminada, sobrante_minimo, activo`
y de solo lectura ⚠️ `cantidad_disponible` y `um` (código de la unidad, ej. `"m"`).

Ajuste de stock (`POST /inventory/movimientos/`):

```json
{ "tipo_item": "producto", "item_id": 4, "cantidad": -2, "tipo_movimiento": "ajuste",
  "motivo": "Conteo físico", "um": "und", "local": 1 }
```

`cantidad` positiva = entrada, negativa = salida. `tipo_movimiento` usa los códigos de
`MovimientoStock.TipoMovimiento` (`ajuste`, `desperdicio`…). El backend debe actualizar la `Existencia`.
Al crear un producto o material con "stock inicial", el frontend primero lo crea y después
envía este mismo POST con `motivo: "Stock inicial"`.

### Ventas y pedidos — `src/features/ventas/api.js`

`/sales/pedidos/` · filtros `estado`, `cliente`

Lee: `id, codigo_pedido, cliente, estado, moneda, total, tipo_cobro, confirmado_en, creado_en, actualizado_en, lineas[]`
y cada línea `id, producto, cantidad, precio_unitario, descripcion`.

Crear (`POST`), con las líneas anidadas (serializer anidado con `create()` propio):

```json
{
  "cliente": 5, "estado": "confirmado", "tipo_cobro": "transferencia", "moneda": "USD",
  "fecha_entrega": "2026-11-20", "notas": "Logo en el pecho", "local": 1,
  "lineas": [{ "tipo_linea": "producto", "producto": 3, "cantidad": 12, "precio_unitario": 15, "moneda": "USD" }]
}
```

Cambiar de estado (tablero, detalle, anular): `PATCH /sales/pedidos/{id}/ { "estado": "en_produccion" }`.
Estados: `cotizado → confirmado → en_produccion → listo → entregado → facturado`, y `anulado`.

El backend debe:
- generar `codigo_pedido` (el frontend muestra `P-1016`) y calcular `total`;
- descontar el stock (`salida_venta`) cuando el pedido pasa de `cotizado` a cualquier estado confirmado,
  y devolverlo si se anula un pedido que ya lo había descontado.

Pendientes ⚠️:
- `fecha_entrega` (DateField, opcional) y `notas` (TextField) **no están** en `PedidoVenta`.
  Son las que alimentan "Próximas entregas" y las etiquetas "Mañana / Vencido" del tablero.
- `descripcion` en cada línea (nombre del producto, `source="producto.nombre"`).
- Opcional: `cliente_nombre` (`source="cliente.nombre"`). Si no viene, el frontend lo busca en `/sales/clientes/`.
- `cliente` puede ser `null` (venta de mostrador), como ya permite el modelo.

### Compras — `src/features/compras/api.js`

`/purchasing/ordenes/` · filtros `estado`, `proveedor`

Lee: `id, proveedor, estado, total, moneda, creado_en, lineas[]` (`material, um, cantidad, precio_unitario, total_linea, descripcion`).

Crear: `{ proveedor, estado, moneda, notas, local, lineas: [{ material, um, cantidad, precio_unitario }] }`.
Cambiar estado: `PATCH { "estado": "confirmada" | "recibida" | "anulada" }`.

El backend debe calcular `total` / `total_linea` y, al pasar a `recibida`, sumar el stock de cada
materia prima (`entrada_compra`).

Pendientes ⚠️: `notas` en `OrdenCompra`; `descripcion` en cada línea (`source="material.nombre"`);
opcional `proveedor_nombre`. El código visible `OC-7` se arma con el `id`.

### Historial — `src/features/historial/Historial.jsx`

`GET /inventory/movimientos/` · filtros `tipo_item`, `tipo_movimiento`, `desde`, `hasta`, `search`

Lee: `id, creado_en, tipo_item, item_id, tipo_movimiento, cantidad, um, motivo` y ⚠️ `item_nombre`,
`usuario_nombre` (agregarlos en el serializer; si falta `item_nombre`, el frontend lo busca en el inventario).

### Auditoría — `src/features/auditoria/api.js`

`GET /audit/acciones/` (solo lectura) · filtros `modulo`, `accion`, `desde`, `hasta`, `search`

Lee: `id, creado_en, usuario, modulo, entidad, entidad_id, accion, estado_anterior, estado_nuevo, direccion_ip`
y ⚠️ `usuario_nombre`. Los valores de `accion` que tienen etiqueta: `login, crear, modificar,
cambiar_estado, anular, eliminar, activar, restablecer_password`; otros se muestran tal cual.

### Usuarios — `src/features/usuarios/api.js`

> Con el PR #3 esto cambia: la ruta es `/core/usuarios/` (por ahora **solo lectura**), los campos
> son `nombre_usuario, correo, nombre, apellido, rol` (un solo rol: `admin`, `gerente`,
> `operario`, `vendedor`), `local, es_global, activo`, y no hay `/roles/`. Hay que adaptar
> `src/features/usuarios/api.js` cuando el PR se acepte.

`/identity/usuarios/` (CRUD) y `GET /identity/roles/`

Lee: `id, username, first_name, last_name, email, es_global, activo, last_login` y ⚠️ `roles`
(lista de códigos de `Rol`, ej. `["vendedor"]`, desde `UsuarioRol`).

Crear: `{ username, first_name, last_name, email, password, es_global, roles: ["vendedor"] }`.
Restablecer contraseña: `PATCH /identity/usuarios/{id}/ { "password": "..." }`.
El backend debe guardarla con `set_password()` y nunca devolverla.

### Dashboard — `src/features/dashboard/api.js`

`GET /reports/dashboard/` devuelve todo calculado (forma exacta en el comentario del archivo):
`resumen`, `ingresosDiarios`, `proximasEntregas`, `stockMateriaPrima`, `stockProductos`, `movimientos`.

### Reportes — `src/features/reportes/api.js`

`GET /reports/resumen/?desde=YYYY-MM-DD&hasta=YYYY-MM-DD` devuelve `totales`, `porProducto`,
`porCliente`, `porMetodo`, `porProveedor` (forma exacta en el comentario del archivo).
Una venta cuenta por su `confirmado_en` y si no está `cotizado` ni `anulado`.

---

## 6. Ejemplo de ViewSet que encaja con el frontend

```python
# sales/views.py
import django_filters
from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer


class ClienteFilter(django_filters.FilterSet):
    desde = django_filters.DateFilter(field_name="creado_en", lookup_expr="date__gte")
    hasta = django_filters.DateFilter(field_name="creado_en", lookup_expr="date__lte")

    class Meta:
        model = Cliente
        fields = ["activo"]


class ClienteViewSet(viewsets.ModelViewSet):
    """CRUD de clientes. DELETE desactiva (borrado lógico)."""

    queryset = Cliente.objects.all().order_by("-id")
    serializer_class = ClienteSerializer
    filterset_class = ClienteFilter
    search_fields = ["nombre", "rif", "telefono", "correo"]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    def perform_destroy(self, instance):
        instance.activo = False
        instance.save(update_fields=["activo", "actualizado_en"])
```

```python
# sales/urls.py
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet

router = DefaultRouter()
router.register("clientes", ClienteViewSet)
urlpatterns = router.urls
```

---

## 7. Lista de verificación al conectar

- [ ] `python manage.py runserver` corre en el puerto 8000 y `npm run dev` en el 5173.
- [ ] Login real: `VITE_AUTH_MOCK=false`, ingresar y ver el nombre del usuario al pie del menú.
- [ ] Con un usuario `es_global=True` aparecen Auditoría y Usuarios; con uno común, no.
- [ ] Por cada módulo: listar, buscar, crear, editar, desactivar y reactivar.
- [ ] Un error de validación del backend aparece debajo del campo.
- [ ] Ventas: crear, avanzar en el tablero, anular; el stock cambia en Inventario.
- [ ] Compras: recibir una orden suma stock de materia prima.
- [ ] Dejar la pestaña abierta más de 30 minutos (vida del access token) y seguir usando: no debe pedir login.
- [ ] Cerrar sesión y abrir una ruta interna: vuelve al login.
