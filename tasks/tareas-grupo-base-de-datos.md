# DLL Sublimados — Asignación de Tareas y Flujos del Grupo de Base de Datos

Documento operativo para la distribución del trabajo del **Grupo de Base de Datos**, diseñado para permitir el desarrollo en paralelo de los 4 integrantes sin conflictos de Git ni colisiones en el código.

---

## 👥 Resumen de Integrantes, Flujos y Ramas

| Integrante | Flujo / Dominio | Apps Django | Rama Git Asignada |
| :--- | :--- | :--- | :--- |
| **Enrrill (Yo)** | Núcleo, Auditoría y Documentación | `core`, `audit`, `documents` | `feature/db-core-audit-enrrill` |
| **Gaby** | Catálogo e Inventario Multi-local | `catalog`, `inventory` | `feature/db-catalog-inventory-gaby` |
| **Luis** | Abastecimiento y Taller de Producción | `purchasing`, `production` | `feature/db-purchasing-production-luis` |
| **Pablo** | Comercial, Precios y Recursos Humanos | `sales`, `pricing`, `hr` | `feature/db-sales-pricing-hr-pablo` |

---

## 🛡️ Reglas de Oro para Trabajar en Paralelo (Cero Colisiones)

1. **Aislamiento de Archivos:** Cada integrante trabaja **únicamente** en los archivos de sus módulos asignados (`backend/apps/<app>/models.py`, `admin.py`), sus DDLs en `database/` y sus seeders en `database/seeders/`. Nadie modifica archivos de otra app.
2. **Relaciones Foráneas por String:** Al definir `ForeignKey` o `ManyToManyField` que apunten a modelos de otro compañero, usar **siempre** la referencia en string:
   ```python
   local = models.ForeignKey('core.Local', on_delete=models.PROTECT, related_name='...')
   producto = models.ForeignKey('catalog.Producto', on_delete=models.CASCADE, related_name='...')
   ```
   *Esto elimina dependencias circulares y permite compilar y migrar sin esperar a que el compañero termine su rama.*
3. **Estándar Obligatorio de Modelos Django:**
   - Heredar de `backend.common.base_models.TimeStampedModel` (`creado_en`, `actualizado_en`) y `backend.common.base_models.ActivoMixin` (`activo = models.BooleanField(default=True)`).
   - Definir explícitamente `class Meta:` con `db_table` en snake_case y nombres plurales/singulares legibles en español:
     ```python
     class Meta:
         db_table = 'inventario_stock'
         verbose_name = 'stock'
         verbose_name_plural = 'stocks'
     ```
   - Tipos de datos estandarizados:
     - Montos monetarios: `models.DecimalField(max_digits=14, decimal_places=2)` + campo `moneda` ('USD', 'VES').
     - Cantidades físicas: `models.DecimalField(max_digits=12, decimal_places=4)`.
     - Porcentajes / factores: `models.DecimalField(max_digits=5, decimal_places=4)`.
4. **Commits y PR:**
   - Seguir estrictamente Conventional Commits (`feat(core): ...`, `feat(catalog): ...`).
   - Todo trabajo se integra hacia `develop` vía Pull Request revisado por el Grupo de Gestión.

---

## 📋 Tareas Detalladas por Integrante

---

### 1. Enrrill (Yo)
**Flujo:** Núcleo, Seguridad, Auditoría y Documentación Transversal  
**Rama:** `feature/db-core-audit-enrrill`  
**Apps:** `backend/apps/core/`, `backend/apps/audit/`, `backend/apps/documents/`

#### 📂 Archivos de Trabajo
- `backend/apps/core/models.py` (completar modelos faltantes)
- `backend/apps/core/admin.py`
- `backend/apps/audit/models.py`
- `backend/apps/audit/admin.py`
- `backend/apps/documents/models.py`
- `backend/apps/documents/admin.py`
- `database/01_nucleo.sql`
- `database/02_auditoria.sql`
- `database/10_documentos.sql`
- `database/seeders/01_seed_nucleo.sql`

#### 📝 Tareas de Modelado y DDL
- [x] **Módulo `core`:**
  - [x] Verificar y ajustar `Local` (`locales`) y `Usuario` (`usuarios`) ya existentes.
  - [x] Implementar modelo `TasaCambio` (`core_tasa_cambio`): fecha de vigencia, tasa USD $\rightarrow$ Bs (`dolares_a_bs`), registrado por (`ForeignKey('core.Usuario')`).
  - [x] Implementar modelo `ContadorCorrelativo` (`core_contador_correlativo`): tipo de comprobante (factura, nota_entrega, orden_produccion, etc.), prefijo, número actual, `local` (`ForeignKey('core.Local')`), control de concurrencia.
- [x] **Módulo `audit`:**
  - [x] Implementar modelo `BitacoraAccion` (`audit_bitacora_accion`): fecha (`creado_en`), usuario (`ForeignKey('core.Usuario')`), local (`ForeignKey('core.Local')`), acción (`INSERT`, `UPDATE`, `DELETE`, `LOGIN`, `APROBACION`), entidad (nombre de la tabla), entidad_id, datos_antes (JSONField), datos_despues (JSONField), ip_origen.
  - [x] Implementar modelo `BitacoraStock` (`audit_bitacora_stock`): fecha, tipo_movimiento (ENTRADA, SALIDA, AJUSTE, TRANSFERENCIA), lote_id, producto_id, cantidad, local_origen_id, local_destino_id, usuario_id, motivo.
- [x] **Módulo `documents`:**
  - [x] Implementar modelo `PlantillaDocumento` (`documents_plantilla`): código, nombre, tipo (FACTURA, NOTA_ENTREGA, ORDEN_PRODUCCION, PRESUPUESTO), contenido_html (con variables dinámicas Jinja/Django), version, activo.
  - [x] Implementar modelo `Documento` (`documents_documento`): correlativo, plantilla (`ForeignKey`), entidad_tipo, entidad_id, generado_por (`ForeignKey('core.Usuario')`), fecha_emision, hash_seguridad, url_archivo.

#### 🌱 Seeders Iniciales (`database/seeders/01_seed_nucleo.sql`)
- [ ] Los 3 locales de la empresa:
  - `L01`: Local Principal (Sede Central - Impresión y Corte)
  - `L02`: Local 2 (Sucursal 2 - Planchado y Confección)
  - `L03`: Local 3 (Sucursal 3 - Diseño y Acabado)
- [ ] Superadministrador (`admin`) y usuarios de prueba para cada rol (`gerente_l1`, `operario_corte`, `vendedor_l1`).
- [ ] Tasa de cambio oficial de arranque (USD/Bs).
- [ ] Registros iniciales de contadores correlativos por local (FAC-000001, NE-000001, OP-000001).
- [ ] Plantillas base HTML para Factura, Nota de Entrega y Presupuesto Comercial.

---

### 2. Gaby
**Flujo:** Catálogo Maestro e Inventario Multi-local  
**Rama:** `feature/db-catalog-inventory-gaby`  
**Apps:** `backend/apps/catalog/`, `backend/apps/inventory/`

#### 📂 Archivos de Trabajo
- `backend/apps/catalog/models.py`
- `backend/apps/catalog/admin.py`
- `backend/apps/inventory/models.py`
- `backend/apps/inventory/admin.py`
- `database/03_catalogo.sql`
- `database/04_inventario.sql`
- `database/seeders/02_seed_catalogo_inventario.sql`

#### 📝 Tareas de Modelado y DDL
- [x] **Módulo `catalog`:**
  - [x] Implementar `Categoria` y `Subcategoria` (`catalog_categoria`, `catalog_subcategoria`).
  - [x] Implementar `UnidadMedida` (`catalog_unidad_medida`): código (`m`, `kg`, `pza`, `rollo`, `cm`), nombre, permite_decimales.
  - [x] Implementar `Talla` (`catalog_talla`): código, nombre, orden.
  - [x] Implementar `Material` (`catalog_material`): código, nombre, categoría, unidad_medida (`ForeignKey`), es_continuo (boolean para telas/rollos), stock_minimo_global.
  - [x] Implementar `Producto` (`catalog_producto`): código, nombre, descripción, subcategoría, tipo (`TERMINADO`, `SEMITERMINADO`, `SERVICIO`).
  - [x] Implementar `VarianteProducto` (`catalog_variante_producto`): producto (`ForeignKey`), talla (`ForeignKey`), color, sku, codigo_barras.
  - [x] Implementar `Servicio` (`catalog_servicio`): nombre, descripción, unidad_medida.
- [x] **Módulo `inventory`:**
  - [x] Implementar `Stock` (`inventory_stock`): local (`ForeignKey('core.Local')`), variante (`ForeignKey`), material (`ForeignKey`, null=True), cantidad_disponible, cantidad_reservada.
  - [x] Implementar `Lote` (`inventory_lote`): material (`ForeignKey`), local (`ForeignKey('core.Local')`), numero_lote, longitud_inicial (para rollos de tela/vinil), longitud_actual, costo_unitario, fecha_vencimiento/ingreso.
  - [x] Implementar `MovimientoStock` (`inventory_movimiento_stock`): tipo (`ENTRADA`, `SALIDA`, `TRANSFERENCIA`), local, cantidad, referencia.
  - [x] Implementar `GuiaTransferencia` y `LineaGuiaTransferencia` (`inventory_guia_transferencia`, `inventory_linea_guia`): codigo_guia (convención ES, antes tracking_code), local_origen, local_destino, estado (`BORRADOR`, `EN_TRANSITO`, `RECIBIDA`, `RECHAZADA`).
  - [x] Implementar `NivelMinimo` (`inventory_nivel_minimo`): local, producto/material, cantidad_minima_alerta.

#### 🌱 Seeders Iniciales (`database/seeders/02_seed_catalogo_inventario.sql`)
- [x] Unidades de medida oficiales: Metros (`m`), Centímetros (`cm`), Kilos (`kg`), Rollos (`rollo`), Piezas (`pza`), Unidades (`und`).
- [x] Tallas: `XS`, `S`, `M`, `L`, `XL`, `XXL` y tallas infantiles (`4`, `6`, `8`, `10`, `12`, `14`, `16`).
- [x] Categorías y Subcategorías: Telas Textiles, Tintas y Químicos, Viniles, Papel de Sublimación, Confección Terminada.
- [x] Catálogo inicial de materiales: Rollo Microdurazno Blanco 1.60m, Tinta Sublimación Cyan/Magenta/Yellow/Black, Vinil Textil Poliuretano, Papel Sublimación 100gr.
- [x] Catálogo de productos: Franela Deportiva Cuello Redondo Sublimada, Taza Blanca 11oz, Gorra Trucker.
- [x] Niveles mínimos de stock para alertas automáticas en L01, L02 y L03.

---

### 3. Luis
**Flujo:** Abastecimiento (Compras) y Taller de Producción Multi-local  
**Rama:** `feature/db-purchasing-production-luis`  
**Apps:** `backend/apps/purchasing/`, `backend/apps/production/`

#### 📂 Archivos de Trabajo
- `backend/apps/purchasing/models.py`
- `backend/apps/purchasing/admin.py`
- `backend/apps/production/models.py`
- `backend/apps/production/admin.py`
- `database/05_compras.sql`
- `database/06_produccion.sql`
- `database/seeders/03_seed_compras_produccion.sql`

> **Nota de implementación:** donde esta lista difiere de la especificación oficial
> (`docs/03` RF-25 a RF-35, `docs/modelo-datos/06.5`–`06.6`, `docs/ddl/06b.5`–`06b.6`),
> se siguió la especificación oficial: el enunciado original se conserva con nombres
> canónicos bajo sus esquemas (`compras.*`, `produccion.*`) y la divergencia se anota
> en cursiva al final de cada punto. Moneda `USD`/`VES` y estados en MAYÚSCULA,
> alineados con `inventory`.

#### 📝 Tareas de Modelado y DDL
- [x] **Módulo `purchasing`:**
  - [x] Implementar `Empresa` y `Proveedor` (`compras.empresa`, `compras.proveedor`): rif, razon_social, direccion, telefono, contacto, calificacion. *Spec 06.5: `nombre` en vez de razon_social, `persona_contacto` en vez de contacto, `moneda_predeterminada` (USD/VES) y `condiciones_pago`.*
  - [x] Implementar `HistorialPrecioProveedor` (`compras.historial_precio_proveedor`): proveedor, material/producto, precio_unitario, moneda, fecha. *Spec 06.5 / RF-28: `empresa` heredada para agrupar por vendedor, `material` (`catalog.Material`), `unidad_medida`, `registrado_en` (`auto_now_add`).*
  - [x] Implementar `OrdenCompra` y `LineaOrdenCompra` (`compras.orden_compra`, `compras.linea_orden_compra`): numero_orden, proveedor, local_destino (`ForeignKey('core.Local')`), estado (`SOLICITADA`, `APROBADA`, `RECIBIDA`, `CANCELADA`), moneda, total. *Spec 06b.5 / RF-26: estados `BORRADOR`, `ENVIADA`, `PARCIAL`, `RECIBIDA`, `CERRADA`, `ANULADA`; líneas con `cantidad_solicitada`, `cantidad_recibida` y `precio_unitario`.*
  - [x] Implementar `RecepcionCompra` y `LineaRecepcionCompra` (`compras.recepcion_compra`, `compras.linea_recepcion_compra`): orden_compra, local, fecha_recepcion, numero_guia_proveedor, observaciones. *Spec 06b.5: estado (`PENDIENTE`, `TOTAL`, `PARCIAL`, `ANULADA`), `observacion`; línea con `lote` opcional para materiales continuos.*
  - [x] Implementar `FacturaCompra` (`compras.factura_compra`): proveedor, numero_factura_control, fecha_emision, monto_total, tasa_cambio_aplicada. *Spec 06.5 / RF-27/29: `numero_externo`, `orden_compra` y `recepcion_compra` opcionales, `tasa_aplicada` (`core.TasaCambio`), `ruta_archivo` para adjunto.*
- [x] **Módulo `production`:**
  - [x] Implementar `Maquina` (`produccion.maquina`): codigo, nombre, tipo (`PLOTTER`, `CALANDRA`, `PLANCHA_TRANSFER`, `COSTURA_RECTA`, `OVERLOCK`), local (`ForeignKey('core.Local')`), horas_operativas, estado (`OPERATIVA`, `EN_MANTENIMIENTO`, `FUERA_SERVICIO`). *Spec 06b.6: tipo (`IMPRESORA`, `PLANCHA`, `CORTADORA`, `OTRO`), estado (`OPERATIVA`, `MANTENIMIENTO`, `INACTIVA`).*
  - [x] Implementar `OrdenProduccion` (`produccion.orden_produccion`): codigo_correlativo, pedido_venta_id (opcional), producto (`ForeignKey('catalog.Producto')`), cantidad, fecha_inicio, fecha_compromiso, estado (`PLANIFICADA`, `EN_PROCESO`, `PAUSADA`, `TERMINADA`, `CANCELADA`). *Spec 06.6 / RF-30/35: `codigo`, `variante` (`catalog.VarianteProducto`), `local_origen`, `fecha_limite`, estados `CREADA`, `EN_PRODUCCION`, `TERMINADA`, `ANULADA`; costeo de cierre obligatorio (`costo_materiales`, `costo_horas`, `costo_total`, `fecha_cierre`).*
  - [x] Implementar `PasoProduccion` (`produccion.paso_produccion`): orden_produccion, orden_secuencia (1, 2, 3), local_ejecucion (`ForeignKey('core.Local')` - ej. L1 corte, L2 planchado), descripcion_tarea, estado (`PENDIENTE`, `EN_PROCESO`, `COMPLETADO`). *Spec 06.6 / RF-31: `orden_paso`, `local`, `trabajador` asignable (`hr.Trabajador`), tipo (`IMPRESION`, `CORTE`, `PLANCHADO`, `CONFECCION`, `DISENO`), estados `PENDIENTE`, `EN_PROCESO`, `TERMINADO`.*
  - [x] Implementar `ConsumoMaterial` (`produccion.consumo_material`): paso_produccion, lote (`ForeignKey('inventory.Lote')`), cantidad_consumida, es_desperdicio (boolean), motivo_merma. *Spec 06b.6 / RF-32/34: tipo (`USO`, `DESPERDICIO`), exclusión mutua estricta `lote` XOR `stock`, `motivo_desperdicio` obligatorio al ser desperdicio, traza débil `movimiento_stock_id`. Hereda `TimeStampedModel` y `ActivoMixin`.*
  - [x] Implementar `OperacionMaquina` (`produccion.operacion_maquina`): maquina, paso_produccion, operador (`ForeignKey('core.Usuario')`), hora_inicio, hora_fin, resultado. *Spec 06.6 / RF-33: `operador_trabajador` (`hr.Trabajador`), `duracion_minutos` y resultado (`COMPLETADO`, `DEFECTUOSO`, `PARCIAL`).*

#### 🌱 Seeders Iniciales (`database/seeders/03_seed_compras_produccion.sql`)
- [x] Proveedores de insumos registrados (telas, tintas, repuestos plóter).
- [x] Parque de máquinas asignadas a cada local:
  - **L01:** Plóter de Sublimación Mimaki/Epson 1.60m, Cortadora Láser Textil.
  - **L02:** Plancha Térmica Industrial 80x100cm, Máquina de Coser Overlock 5 Hilos, Máquina Recta.
  - **L03:** Estampadora Combo 8 en 1 (Gorras, Tazas, Platos), Plancha de Transfer manual.
- [x] Datos de prueba de órdenes de compra y órdenes de producción piloto demostrando el salto de ruta multi-local L1 $\rightarrow$ L2.
- [ ] Carga en una BD limpia: *pendiente de la ejecución secuencial completa con seeders de núcleo (01) y catálogo (02).*

---

### 4. Pablo
**Flujo:** Comercialización (Ventas), Precios y Personal (RRHH)  
**Rama:** `feature/db-sales-pricing-hr-pablo`  
**Apps:** `backend/apps/sales/`, `backend/apps/pricing/`, `backend/apps/hr/`

#### 📂 Archivos de Trabajo
- `backend/apps/sales/models.py`
- `backend/apps/sales/admin.py`
- `backend/apps/pricing/models.py`
- `backend/apps/pricing/admin.py`
- `backend/apps/hr/models.py`
- `backend/apps/hr/admin.py`
- `database/07_ventas.sql`
- `database/08_precios.sql`
- `database/09_rrhh.sql`
- `database/seeders/04_seed_ventas_precios_rrhh.sql`

> **Nota de implementación:** donde esta lista difiere de la especificación oficial
> (`docs/03` RF-36 a RF-48, `docs/modelo-datos/06.7`–`06.9`, `docs/ddl/06b.7`–`06b.9`),
> se siguió la especificación: el enunciado original se conserva y la divergencia
> se anota en cursiva al final de cada punto. Moneda `USD`/`VES` y estados en
> MAYÚSCULA, alineados con `inventory`.

#### 📝 Tareas de Modelado y DDL
- [x] **Módulo `sales`:**
  - [x] Implementar `Cliente` (`ventas.cliente`): tipo_documento (`V`, `E`, `J`, `G`), numero_documento, nombre_razon_social, direccion, telefono, correo, limite_credito. *Implementado según 06.7: nombre, telefono, correo y rif; sin tipo_documento, direccion ni limite_credito.*
  - [x] Implementar `PedidoVenta` (`ventas.pedido_venta`): numero_pedido, cliente, local_venta (`ForeignKey('core.Local')`), vendedor (`ForeignKey('hr.Trabajador')`), estado (`COTIZADO`, `CONFIRMADO`, `EN_PRODUCCION`, `LISTO`, `ENTREGADO`, `FACTURADO`, `ANULADO`), moneda, total_neto, iva, total_bruto. *06.7: un solo `total` (neto/IVA se calculan en servicios), `codigo` en vez de numero_pedido, `local` en vez de local_venta, vendedor como referencia débil, más `confirmado_en`, `fecha_compromiso` y `motivo_anulacion` (obligatorio al anular, RF-43).*
  - [x] Implementar `LineaPedido` (`ventas.linea_pedido`): pedido, producto (`ForeignKey('catalog.Producto')`), variante (`ForeignKey('catalog.VarianteProducto', null=True)`), cantidad, precio_unitario, subtotal. *06.7: `tipo_linea` (PRODUCTO, PRODUCTO_PERSONALIZADO, SERVICIO_PURO), variante | servicio, medida + unidad, moneda, `item_precio` (ref. débil a la matriz) y nota; sin `subtotal` persistido.*
  - [x] Implementar `Cobro` (`ventas.cobro`): pedido, metodo_pago (`EFECTIVO_USD`, `PAGO_MOVIL`, `TRANSFERENCIA_BS`, `PUNTO_VENTA`, `ZELLE`), monto_moneda_original, tasa_cambio_aplicada, monto_usd_equivalente, referencia_bancaria. *RF-42 manda: metodo (`EFECTIVO`, `PUNTO`, `TRANSFERENCIA`, `DIVISA`), monto + moneda, `tasa_aplicada` (obligatoria en Bs.), referencia, fecha y `anulado_en`; admite cobros parciales.*
  - [x] Implementar `FacturaVenta` (`ventas.factura`): numero_control, pedido, fecha_emision, total_usd, total_bs. *06.7 / RF-40: numero + anio + tipo (PROPIA, FISCAL) + local, estado (EMITIDA, ANULADA), total + moneda, `emitida_por`; correlativo único por (tipo, local, año, número).*
- [x] **Módulo `pricing`:**
  - [x] Implementar `ParametroFormula` (`precios.parametro_formula`): clave (`MARGEN_GANANCIA`, `IVA`, `DESCUENTO_MAYORISTA`), valor_numerico, descripcion. *RF-45: vigencia por fechas (`fecha_desde` única, `fecha_hasta`) con `porcentaje_margen` y `porcentaje_iva`.*
  - [x] Implementar `ItemMatrizPrecios` (`precios.item_matriz_precios`): producto/servicio, unidad_medida, rango_cantidad_min, rango_cantidad_max, precio_base, precio_final_sugerido. *RF-44: sin rangos de cantidad; destino exclusivo producto | variante | servicio, material condicionante, medida + unidad, moneda, margen e IVA; el precio final no se persiste.*
  - [x] Implementar `HistorialCambioPrecio` (`precios.historial_cambio_precio`): matriz_item, precio_anterior, precio_nuevo, modificado_por (`ForeignKey('core.Usuario')`), justificacion. *06.8: `item_matriz` + `usuario` + `cambiado_en`; append-only (save/delete bloquean). Hereda `TimeStampedModel` y `ActivoMixin` (estándar del grupo).*
- [x] **Módulo `hr`:**
  - [x] Implementar `Trabajador` (`rrhh.trabajador`): cedula, nombres, apellidos, cargo (`VENDEDOR`, `OPERARIO_CORTE`, `OPERARIO_PLANCHA`, `DISENADOR`, `GERENTE`), telefono, correo, fecha_ingreso. *06.9 / RF-48: `nombre_completo` (sin cedula/nombres/apellidos), cargo (`IMPRESOR`, `VENDEDOR`, `DISENADOR`, `PLANCHADOR`, `CONFECCIONADOR`, con CHECK en BD) y referencia débil opcional a `core.Usuario`.*
  - [x] Implementar `TrabajadorLocal` (`rrhh.trabajador_local`): trabajador, local (`ForeignKey('core.Local')`), porcentaje_comision_venta, es_local_principal. *06.9: `es_principal` (uno por trabajador, unique parcial); comisión diferida con la nómina (RF-49).*

#### 🌱 Seeders Iniciales (`database/seeders/04_seed_ventas_precios_rrhh.sql`)
- [x] Clientes base: Cliente genérico "Consumidor Final" y 2 clientes corporativos de prueba.
- [x] Parámetros base de fórmulas comerciales:
  - Margen de ganancia: `1.30` (+30%).
  - Alícuota de impuesto: `0.16` (16% IVA).
  - Factor de conversión estándar: *no aplica en `pricing`; la conversión USD/Bs usa `core.TasaCambio`.*
  - [ ] Carga en una BD limpia: *pendiente de `database/seeders/01_seed_nucleo.sql` (Enrrill), que debe crear el usuario `admin`; sin él el seeder omite la fila de `precios.parametro_formula` con aviso y basta re-ejecutarlo.*
- [x] Matriz de precios inicial para prendas estándar y servicios de sublimación por metro.
- [x] Fichas de trabajadores y vendedores asignados a los locales L01, L02 y L03.

---

## 🚀 Flujo de Trabajo Git Paso a Paso para Cada Integrante

### 1. Ubicarse en su rama asignada
```bash
# Ejemplo para Enrrill:
git checkout feature/db-core-audit-enrrill

# Ejemplo para Gaby:
git checkout feature/db-catalog-inventory-gaby

# Ejemplo para Luis:
git checkout feature/db-purchasing-production-luis

# Ejemplo para Pablo:
git checkout feature/db-sales-pricing-hr-pablo
```

### 2. Implementar modelos y verificar calidad
```bash
# Verificar que Django reconozca los modelos y sintaxis
python manage.py check

# Generar y aplicar migraciones de prueba en local
python manage.py makemigrations
python manage.py migrate

# Validar estilo de código
flake8 backend/
```

### 3. Guardar cambios (Conventional Commits)
```bash
git add backend/apps/<tu-modulo>/ database/
git commit -m "feat(<modulo>): implementa modelos de datos y scripts ddl" -m "- crea tablas con class Meta db_table explícito" -m "- agrega seeder inicial con datos base del negocio"
git push origin <nombre-de-tu-rama>
```

### 4. Abrir Pull Request
- Crear el PR apuntando hacia `develop`.
- Notificar al Grupo de Gestión para su revisión y merge.
