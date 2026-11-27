---
status: borrador
type: documento
tags:
  - negocio
  - locales
  - especificacion
created: 2026-11-04
version: 0.2
---

# 02 Descripción del negocio y locales

Quién es el negocio, cómo trabaja cada local y qué fluye entre ellos. Define el contexto operacional que después se modela en [03 Requerimientos del sistema](03-requerimientos-del-sistema.md) y [05 Flujos de proceso](05-flujos-de-proceso.md).

## El negocio

Se dedica a la **sublimación, planchado y confección de prendas y otros objetos** personalizados: franelas, tazas, banderas, rótulos, entre otros. Trabaja bajo pedido del cliente, con dos vertientes:

- **Producto personalizado** sublimado o planchado: se parte de materia prima (tela, vinil, tazas, papel) y se transforma.
- **Servicio puro**: diseño de artes, planchado sobre material que trae el cliente.

Opera en **3 locales** físicos conectados por internet al mismo sistema y base de datos.

## Locales y sus funciones

| Local | Actividad principal | Rol en la cadena |
| --- | --- | --- |
| **Local principal (L1)** | Impresión, corte | Transforma materia prima: imprime diseños sobre el rollo/medida, corta a medida. Abastece a los locales 2 y 3 con piezas o rollos cortados para planchar/confeccionar. |
| **Local 2 (L2)** | Planchado, confección y diseño | Recibe material semi-procesado de L1, plancha o confecciona el producto final. Genera diseños digitalmente. |
| **Local 3 (L3)** | Planchado, confección y diseño | Igual que L2; local de servicio de otra zona, descongestiona demanda y atiende clientes cercanos. |

## Qué fluye entre locales

1. **Material para transformar**: L1 envía a L2/L3 piezas impresas/cortadas a medida o material en tránsito para procesar. Se rastrea con entradas por **transferencia** en inventario.
2. **Pedidos multi-local**: un pedido de cliente puede originarse en cualquier local y necesitar pasos de producción en varios. La **ruta de producción** orquesta los pasos por local ([05 Flujos de proceso](05-flujos-de-proceso.md#flujo-2--producción-multi-local-el-más-crítico)).
3. **Stock compartido**: si a un local se le acaba una talla o material, pide transferencia al local que sí lo tiene.
4. **Diseños de L2/L3** alimentan la impresión de L1: los archivos de arte son gestionados directamente por el diseñador de forma externa al sistema.
5. **Comisiones** *(diferidas con la nómina, [09 Decisiones diferidas y fases](09-decisiones-diferidas-y-fases.md))*: en fase 1 solo se registra quién cierra cada pedido (`vendedor_trabajador_id`); la acumulación, liquidación y pago de comisiones va en fase posterior.

## Usuarios del sistema

| Rol (tipo) | Alcance | Qué hace típico |
| --- | --- | --- |
| Dueño / Admin | Global, todos los locales | Módulo de administración (bitácoras), reportes consolidados, RRHH, tipo de cambio del día, configuración |
| Gerente de local | 1 local | Ventas de su local, compras de su local, producción, reporte de su local |
| Operario de producción | 1 local | Registrar consumo de material por medición, operaciones de su máquina |
| Vendedor / Cajero | 1 local | Clientes, pedidos, factura propia, nota de entrega |
| Trabajador (sin login avanzado) | Puede o no tener login | Registro de quién hace qué (cargo y local); en fase 1 sin consulta de comisiones (nómina diferida) |

> Los roles se detallan en [04 Arquitectura del monolito modular](04-arquitectura-del-monolito-modular.md#seguridad-y-permisos) y en [03 Requerimientos del sistema](03-requerimientos-del-sistema.md#1-identity--login-registro-y-usuarios).

## Ciclo de vida de un pedido típico

```mermaid
flowchart LR
    A[Cliente llega] --> B[Vendedor cotiza con la matriz de precios]
    B --> C[Pedido confirmado]
    C --> D[Orden de producción]
    D --> E[L1 imprime y corta]
    E --> F[L2 o L3 planchan y confeccionan]
    F --> G[Producto en stock]
    G --> H[Entrega y factura propia]
    H --> I[Comisión acumulada]
```

El detalle paso a paso está en [05 Flujos de proceso](05-flujos-de-proceso.md). En texto: cliente llega al local → vendedor toma medidas/especificaciones y consulta la **matriz de precios** → pedido confirmado → se genera la **orden de producción** con su ruta por local → cada local consume material por medición y registra operaciones de máquina → el producto queda en stock del último local → cliente retira o se entrega con nota de entrega → se emite **factura propia** → la comisión se acumula al trabajador que atendió/produjo.

## Referencias

- [Glosario](referencias/glosario-del-negocio.md)
- [05 Flujos de proceso](05-flujos-de-proceso.md)
- [04 Arquitectura del monolito modular](04-arquitectura-del-monolito-modular.md)