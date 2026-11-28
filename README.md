# DLL Sublimados — Core

Sistema integral de gestión para el negocio **DLL Sublimados** (sublimación, planchado y confección de prendas y objetos personalizados), distribuido en 3 locales y conectado a un servidor central.

Consta de un backend monolítico modular en **Django 6 + PostgreSQL** (organizado en `backend/apps/` con `manage.py` en la raíz) y una SPA en **React 19 + JavaScript + Vite + Tailwind CSS** (en `frontend/`).

---

## 📚 Documentación del sistema

Toda la especificación técnica, modelos de datos, diagramas Mermaid y normativas viven en el directorio [`docs/`](docs/00-indice-del-sistema.md):

| Documento | Descripción |
| --- | --- |
| [00 Índice del sistema](docs/00-indice-del-sistema.md) | Catálogo completo de los 14 documentos de especificación. |
| [01 Resumen ejecutivo](docs/01-resumen-ejecutivo.md) | Visión del negocio, alcance, locales y las 11 apps. |
| [04 Arquitectura del monolito modular](docs/04-arquitectura-del-monolito-modular.md) | Organización de backend, frontend y reglas de comunicación. |
| [06 Modelo de datos](docs/06-modelo-de-datos.md) | MER transversal y detalle por esquema (`docs/modelo-datos/`). |
| [08 Estructura del frontend](docs/08-estructura-del-frontend.md) | Arquitectura de la SPA: layout, providers, features y componentes. |
| [10 Git Flow y normas del equipo](docs/10-git-flow-y-normas-del-equipo.md) | Ramas (`main`, `testeo`, `develop`, `feature/*`), roles y flujo de PR. |
| [11 Normas de código y POO](docs/11-normas-de-codigo-y-poo.md) | Paradigma POO, PEP 8, docstrings obligatorios y checklist. |
| [13 Instalación y entorno local](docs/13-instalacion-y-entorno-local.md) | Guía de puesta en marcha paso a paso para backend y frontend. |
| [14 Convenciones de commits](docs/14-convenciones-de-commits.md) | Estándar Conventional Commits con títulos imperativos y desglose en viñetas. |

---

## 🚀 Inicio rápido (Desarrollo local)

### Requisitos previos

- Python 3.12+
- PostgreSQL 14+
- Node.js 20+ y npm

### 1. Backend (Django)

```bash
# 1. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate       # En Linux/macOS
# .\venv\Scripts\Activate.ps1  # En Windows PowerShell

# 2. Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Base de datos PostgreSQL (ver database/00_crear_bd.sql)
psql -U postgres -f database/00_crear_bd.sql

# 4. Configurar variables de entorno
cp .env.example .env

# 5. Migraciones limpias y datos iniciales
python manage.py migrate
psql -U postgres -d dll_sublimados -f database/01_datos_iniciales.sql

# 6. Crear superusuario y levantar servidor
python manage.py createsuperuser
python manage.py runserver
```

La API estará disponible en `http://localhost:8000/api/v1/` y el administrador en `http://localhost:8000/admin/`.

### 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

La SPA estará disponible en `http://localhost:5173`. Las llamadas a `/api` se redirigen automáticamente al backend.

---

## 🛠️ Herramientas de calidad

```bash
# Verificación de estilo PEP 8
flake8 backend/ manage.py

# Formateo de código Python
black --check backend/ manage.py

# Orden de imports
isort --check-only backend/ manage.py

# Pruebas automatizadas
pytest

# Compilación de frontend
cd frontend && npm run build
```

---

## 📝 Convenciones de commits

El proyecto exige el uso estricto de **Conventional Commits**:

```text
<tipo>(<ámbito>): <título en imperativo, minúscula, sin punto final>

- <descripción detallada del cambio 1>
- <descripción detallada del cambio 2>
- <descripción detallada del cambio 3>

Refs: RF-XX
```

Consulta [14 Convenciones de commits](docs/14-convenciones-de-commits.md) para la lista completa de tipos, ámbitos válidos y ejemplos.

---

## 📄 Licencia

Este proyecto es de carácter académico y está destinado al uso exclusivo en la evaluación de la materia **Lenguajes de Programación III**.

