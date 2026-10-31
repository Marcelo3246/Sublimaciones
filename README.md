# Sistema Web de Gestión Comercial para Negocio de Sublimación 

Un sistema web enfocado en la automatización, centralización y control eficiente de las operaciones comerciales de un negocio de productos personalizados y sublimación.

---

## 📖 Descripción del Proyecto

El crecimiento en las operaciones de los negocios de sublimación exige un control preciso sobre las ventas, la disponibilidad de insumos y la relación con los proveedores. Este proyecto surge como solución a la necesidad de abandonar los registros manuales o descentralizados para dar paso a una plataforma web integrada.

El sistema permite gestionar de manera unificada:
* **Control de Ventas e Ingresos:** Registro detallado de transacciones comerciales e historial de operaciones.
* **Gestión de Inventarios y Recursos:** Monitoreo en tiempo real de insumos críticos (tintas, papel, prendas, etc.) y productos terminados.
* **Administración de Proveedores:** Catálogo organizado de proveedores y registro de compras.
* **Seguridad y Control de Acceso:** Gestión de usuarios con roles y permisos diferenciados.
* **Reportes e Informes:** Generación de consultas clave para la toma de decisiones.

---

## 🏗️ Paradigma de Desarrollo: POO

Para garantizar la escalabilidad y el mantenimiento del sistema, este proyecto se rige estrictamente por el paradigma de **Programación Orientada a Objetos (POO)**. 

* **Encapsulamiento:** Protección de los datos sensibles en las clases (ej. contraseñas de usuarios).
* **Herencia y Polimorfismo:** Reutilización de código a través de clases base (ej. una clase `Persona` de la cual heredan `Usuario`, `Cliente` y `Proveedor`).
* **Abstracción:** Modelado de entidades del mundo real (Venta, Producto, Insumo) en modelos de Django.

> **[📝 NOTA PARA EL ALUMNO: Inserta aquí una imagen del Diagrama de Clases (UML) de tu proyecto]**
> <p align="center">
>   <img src="docs/diagrama_clases_poo.png" alt="Diagrama de Clases POO" width="800"/>
> </p>

---

## 👥 Organización Estructural (Equipos de Clase)

Para el éxito de este proyecto masivo, el desarrollo se ha fragmentado y asignado a distintos grupos del salón. La comunicación y el respeto por los límites de cada equipo son vitales.

1. **🛡️ Grupo de Gestión (Nuestro Grupo):** Administradores absolutos del repositorio (DevOps/Scrum Masters). Encargados de revisar, aceptar y fusionar (Merge) el código de los demás. Supervisores del cumplimiento del Git Flow.
2. **💾 Grupo de Base de Datos:** Responsables del diseño del modelo Entidad-Relación, scripts en SQL y configuración de los modelos en SQLite/Django.
3. **⚙️ Grupo de Backend:** Encargados de programar la lógica de negocio, controladores (Views en Django) y aplicar las normas de POO.
4. **🎨 Grupo de Frontend:** Desarrolladores de las interfaces de usuario (HTML, CSS, JavaScript) y maquetación web.
5. **🧪 Grupo de Testing y Calidad:** Responsables de probar los módulos antes de pasar a la rama principal.

---

## 📜 Normas Obligatorias para el Éxito del Proyecto

Para evitar conflictos de código, pérdida de avances y asegurar un entorno de trabajo profesional, **TODOS los grupos deben firmar y cumplir** las siguientes normativas:

### 1. Políticas Estrictas de Repositorio
* 🚫 **PROHIBICIÓN TOTAL:** Ningún estudiante (fuera del grupo de Gestión) puede hacer un `commit` o `push` directo a las ramas `main`, `testeo` o `develop`. 
* Todo nuevo código debe ingresar obligatoriamente a través de un **Pull Request (PR)**.
* Los PR solo serán revisados y aprobados por el **Grupo de Gestión**. Si un PR rompe el código actual, será rechazado inmediatamente.

### 2. Estándares de Código y POO
* El código fuente (Python) debe respetar el estándar de estilo **PEP 8**.
* Todo método, clase o función debe contener comentarios técnicos (*Docstrings*) explicando qué hace, qué recibe y qué retorna.
* Está prohibido el uso de variables globales innecesarias; todo debe estar encapsulado en sus respectivas clases.

### 3. Resolución de Conflictos
* Antes de solicitar un PR, el desarrollador **debe** actualizar su rama local con la última versión de `develop` (`git pull origin develop`) y resolver cualquier conflicto de fusión (Merge Conflict) en su propia computadora.

> **[📝 NOTA PARA EL ALUMNO: Inserta aquí una captura de pantalla de un ejemplo de código bien documentado o de un Pull Request en GitHub]**
> <p align="center">
>   <img src="docs/ejemplo_buenas_practicas.png" alt="Buenas prácticas de código" width="600"/>
> </p>

---

## 🌿 Flujo de Trabajo: Git Flow

Este proyecto utiliza la estrategia de ramificación **Git Flow** adaptada con una rama de testeo integral. Todo estudiante debe conocer la estructura y los comandos.

<p align="center">
  <img src="docs/ramas git flow.png" alt="Ramas Git Flow" width="800"/>
</p>

<p align="center">
  <img src="docs/gitflow_diagram.png" alt="Diagrama Git Flow - Sistema de Sublimación" width="800"/>
</p>

### Estructura de Ramas

| Rama | Propósito | Origen | Destino final |
|------|-----------|--------|---------------|
| `main` | Versión estable y final del proyecto (producción). | — | — |
| `testeo` | Copia de `main`. Se usa para **probar todo el proyecto integrado** antes de subir cambios a `main`. | `main` | `main` |
| `develop` | Rama de integración para **probar módulos individuales** de cada equipo. | `testeo` | `testeo` |
| `feature/*` | Ramas de trabajo de cada equipo para desarrollar funcionalidades específicas. | `develop` | `develop` |
| `hotfix/*` | Correcciones urgentes en producción. | `main` | `main` y `testeo` |

### Flujo general del proyecto

```text
feature/* ──PR──▶ develop (prueba de módulos individuales)
                      │
                      ▼
               develop ──PR──▶ testeo (prueba del proyecto completo)
                                    │
                                    ▼
                             testeo ──PR──▶ main (versión final / entrega)
```

> **⚠️ IMPORTANTE:** La rama `testeo` es una **copia de `main`** y solo recibe código que ya fue probado en `develop`. Al finalizar el proyecto, el contenido de `testeo` se fusiona a `main` como entrega final.

### Comandos de uso diario por los equipos:

**1. Crear la rama para tu módulo (Desde develop):**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/nombre-de-tu-tarea
```
*(Ejemplos: `feature/modelo-bd`, `feature/vistas-backend`, `feature/ui-ventas`)*

**2. Guardar y subir tu trabajo:**
```bash
git add .
git commit -m "feat: agrega clase Producto con POO"
git push origin feature/nombre-de-tu-tarea
```

**3. Crear un Pull Request:**
- Las ramas `feature/*` hacen PR hacia `develop`.
- Una vez probados los módulos en `develop`, el **Grupo de Gestión** hace PR de `develop` hacia `testeo`.
- Al finalizar las pruebas integrales en `testeo`, el **Grupo de Gestión** hace PR de `testeo` hacia `main`.

**4. Crear un Hotfix (Solo emergencias en producción):**
```bash
git checkout main
git checkout -b hotfix/solucion-error-critico
```
> Los hotfixes se fusionan tanto a `main` como a `testeo` para mantener ambas ramas sincronizadas.

---

## 📦 Módulos del Sistema y Estructura

- **Usuarios:** Gestión, roles y control de acceso.
- **Productos:** Inventario de insumos.
- **Ventas:** Registro y facturación.
- **Proveedores:** Compras y abastecimiento.
- **Reportes:** Generación de informes.

```text
proyecto-sublimacion/
├── docs/                    # Documentación, diagramas e imágenes
├── database/                # Scripts SQL 
├── src/                     # Código fuente Django
└── tests/                   # Pruebas unitarias
```

---

## 💻 Tecnologías Utilizadas

* **Lenguaje:** Python (Orientado a Objetos)
* **Backend:** Django Framework
* **Frontend:** HTML / CSS / JavaScript
* **Base de Datos:** SQLite
* **Control de Versiones:** Git / GitHub
* **Gestión de Tareas:** Trello

---
## 📄 Licencia
Este proyecto es de carácter académico y está destinado al uso exclusivo en la evaluación de la materia Lenguajes de Programación III.