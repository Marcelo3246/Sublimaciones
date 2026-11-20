---
status: borrador
type: documento
tags:
  - base-de-datos
  - convenciones
  - postgresql
  - django
created: 2026-11-04
version: 0.3
---

# 07 Convenciones de base de datos

Reglas de implementación para PostgreSQL a través de los modelos Django. Se aplican a las entidades de los 11 módulos descritos en [06 Modelo de datos](06-modelo-de-datos.md).

## Naming y esquema

| Regla | Ejemplo |
| --- | --- |
| **Un esquema de PostgreSQL por módulo**, mismo nombre que la app Django: `catalogo.material`, `ventas.pedido_venta`, `inventario.lote` (Detalle en [06b Esquemas y DDL PostgreSQL](06b-esquemas-y-ddl-postgresql.md)) | Reemplaza el prefijo de tabla; delimita el dominio y evita colisiones |
| Modelos y tablas en español, snake_case, en singular: `PedidoVenta`, `Lote`, `GuiaTransferencia` | Tabla final vía `Meta.db_table`: `ventas.pedido_venta` o `pedidos_venta` |
| Columnas en español, snake_case, sin abreviaturas ambiguas y **sin tilde/ñ en identificadores** (`anio`, no `año`): `cantidad`, `precio_unitario`, `fecha_vigencia` | Legible para el equipo y el servidor |
| Llaves foráneas: el campo se llama `<tabla>` y Django genera `<tabla>_id` (`proveedor_id`, `local_origen_id`) | Igual que genera Django |
| Booleanos con estilo Django (única excepción al español): `is_active`, `is_global` | `is_active = false` es el borrado lógico |
| Contraints UNIQUE compuestos con sufijo `_uk` (`factura_correlativo_uk`) | Nombres de constraint explícitos |
| La lógica de código que no es modelo (funciones, servicios, componentes React) **sí va en inglés** | `consume_material()`, `usePartida()`→`useLote()`, `<PriceMatrix />` |

### Estructura obligatoria de `class Meta` en los modelos

Para evitar que Django genere tablas con prefijos planos ambiguos (`catalog_material`) en el esquema por defecto, **todo modelo implementado por el Grupo de Base de Datos debe definir su `class Meta`**:

```python
from django.db import models
from backend.common.base_models import ActivoMixin, TimeStampedModel

class Material(TimeStampedModel, ActivoMixin):
    nombre = models.CharField("nombre", max_length=150)
    codigo = models.CharField("código", max_length=50, unique=True)

    class Meta:
        db_table = "materiales"  # Nombre explícito de tabla en BD
        verbose_name = "material"
        verbose_name_plural = "materiales"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
```

## Tipos de datos

| Dato | Tipo | Notas |
| --- | --- | --- |
| Montos monetarios | `NUMERIC(14, 2)` + columna `moneda` (`USD` \| `BS`), nunca float | `DecimalField(max_digits=14, decimal_places=2)` |
| Cantidades de material | `NUMERIC(12, 4)` | Metros con décimas: 1.8 m, 0.35 m² |
| Porcentajes (margen, IVA, comisión) | `NUMERIC(5, 4)` | `1.3000` = 130 %, `0.1600` = 16 % |
| Textos de negocio | `VARCHAR(n)` con tamaño razonable | Sin `TEXT` donde un `VARCHAR` basta |
| Estado previo/posterior de datos | `JSONB` (con opción de índice GIN) | Snapshot de eventos auditados |
| Rutas de archivos | `FileField` | Los PDFs emitidos viven en disco del servidor, registrados en la tabla del documento |
| UUIDs | Solo para referencias externas (códigos públicos de guía de transferencia, seguimiento externo) | Claves primarias internas: `BigAutoField` |

## Reglas que cruzan todas las tablas de negocio

1. **Auditable**: `creado_en`, `actualizado_en`, `creado_por_id` (FK a usuario), `is_active` (borrado lógico). Las tablas de movimiento de stock agregan `tipo_movimiento` y `motivo` (quién movió y por qué).
2. **Borrado lógico**: nunca `DELETE` físico de datos de negocio. El registro "se elimina" poniendo `is_active = false`; las consultas normales filtran `is_active = true` (con acceso al histórico solo con permiso).
3. **Append-only para bitácoras**: `bitacora_accion` y `bitacora_stock` no tienen `update` ni `delete` en el ORM, y quedan bloqueadas a nivel de permisos de base de datos.
4. **Numeración correlativa por (tipo, local, año)** con secuencia de BD + lock (`SELECT ... FOR UPDATE`), para facturas, orden de producción, guía de transferencia y comprobante de comisión.
5. **Multi-moneda**: todo monto lleva su `moneda`; el conversor usa la tabla `tasa_cambio` con el tipo de cambio del día; el monto en Bs es el equivalente calculado, no un campo secundario duplicado.
6. **Movimientos de stock = transacción atómica**: descuento del origen, entrada del destino, registro en `bitacora_stock` y enlace con la guía de transferencia se graban en la misma transacción de BD.
7. **La fórmula de precio no se completa en triggers**: `precio_base × porcentaje_margen × porcentaje_iva` ocurre en el código (capa de servicios de `pricing`); la BD garantiza `CHECK (porcentaje_margen > 0)` y `CHECK (porcentaje_iva >= 0)`.
8. **Excepción documentada — `cobro.anulado_en`**: la tabla `ventas.cobro` usa `is_active = false` como borrado lógico estándar (cobro anulado), y complementa con `anulado_en TIMESTAMPTZ` para registrar el momento exacto de anulación. Es la única tabla con este campo adicional; el patrón no se replica a otras tablas.

## Referencias débiles (polimórficas)

Cuando una tabla apunta genéricamente a entidades de distintos módulos sin FK rígida, se usa el patrón `<contexto>_tipo` + `<contexto>_id`:

| Campo tipo | Campo id | Tabla | Qué representa |
| --- | --- | --- |---|
| `entidad_tipo` | `entidad_id` | `auditoria.bitacora_accion`, `documentos.documento` | Tipo y ID del objeto auditado/referenciado |
| `tipo_item` | `item_id` | `auditoria.bitacora_stock` | Material o variante afectada |
| `documento_origen_tipo` | `documento_origen_id` | `inventario.movimiento_stock` | Documento que originó el movimiento |

Regla: el nombre del campo `tipo` siempre describe el contexto específico (nunca `tipo` a secas); el campo `id` acompaña con el mismo prefijo.

## Índices y performance

| Índice | Sobre | Para qué |
| --- | --- | --- |
| `(local_id, material_id, variante_id)` funcional con `COALESCE`, WHERE `is_active` | `inventario.stock` | Una sola fila de saldo por clave; vistas de stock por local |
| `(local_id, material_id, estado)` | `inventario.lote` | Resolución de lotes disponibles |
| `(codigo_lote)` UNIQUE | `inventario.lote` | Trazabilidad del rollo |
| `(local_id, creado_en DESC)` | `inventario.movimiento_stock` | Historial de stock en orden inverso |
| `(estado, local_id)` | `ventas.pedido_venta`, `produccion.orden_produccion` | Tableros de pedidos y producción |
| `(tipo_documento, local_id, anio, numero)` UNIQUE | `documentos.documento` | Numeración correlativa y repositorio |
| `(cargo) WHERE is_active` | `rrhh.trabajador` | Catálogo de personal activo por cargo |
| `(material_id, proveedor_id, registrado_en DESC)` | `compras.historial_precio_proveedor` | Comparador de precios |
| `(usuario_id, creado_en DESC)` | `auditoria.bitacora_accion` | Bitácora de usuario en orden inverso |
| `(tipo_item, item_id, creado_en DESC)` | `auditoria.bitacora_stock` | Bitácora de stock |

## Integridad y estados

- **Estados de negocio** (lote, pedido, transferencia) se representan con `VARCHAR(n)` + constraint `CHECK` en BD; en Django, mediante `TextChoices`. Evita estados inválidos a cualquier nivel.
- **La máquina de estados del pedido** (`cotizado → confirmado → en_produccion → listo → entregado → facturado`) se regula en la capa de servicios; la BD solo asegura el CHECK.
- FK cruzadas entre esquemas solo si son relación de negocio declarada ([06 Modelo de datos](06-modelo-de-datos.md)); de lo contrario se guarda solo el `id` (sin FK) para respetar el límite del módulo.
- **`tasa_cambio` y `contador_correlativo` viven en `nucleo`**: son infraestructura común. Lecturas de otras apps van vía la capa de servicios o FK de lectura (cobro guarda `tasa_aplicada_id` como evidencia de la tasa usada).
- Sin triggers de negocio en fase 1: la lógica vive en los servicios de Django. Los triggers quedan como herramienta de refuerzo si la auditoría requiere bloqueo absoluto.

## Migraciones y esquemas

- Cada módulo aplica `makemigrations`/`migrate` de su app; las migraciones se ejecutan en orden de dependencia (nucleo primero).
- Django termina escribiendo el esquema con `Meta.db_table = 'ventas.pedido_venta'`; no se usan `search_path` ni bases de datos separadas — todo el negocio vive en una BD, dividida por esquemas ([06b Esquemas y DDL PostgreSQL](06b-esquemas-y-ddl-postgresql.md)).

## Backups y ambiente

- Backup diario `pg_dump` comprimido, con retención de 30 días; probado cada mes (RNF-06). El `pg_dump` captura **todos los esquemas** en un solo volcado.
- 3 ambientes: `dev`, `staging` (opcional), `prod` con credenciales separadas y variables de entorno.

## Referencias

- [06 Modelo de datos](06-modelo-de-datos.md)
- [Glosario](referencias/glosario-del-negocio.md)
- [03 Requerimientos del sistema](03-requerimientos-del-sistema.md)