---
status: borrador
type: documento
tags:
  - instalacion
  - entorno
  - venv
  - despliegue
  - especificacion
created: 2026-11-15
version: 0.1
---

# 13 Instalación y entorno local

Cómo poner el proyecto en marcha en una máquina de desarrollo, qué variables de entorno necesita y cómo está organizado el repositorio. El uso del entorno virtual es **obligatorio** (ver [11 Normas de código y POO](11-normas-de-codigo-y-poo.md)).

## Requisitos previos

| Herramienta | Versión | Para qué |
| --- | --- | --- |
| Python | 3.12+ | Backend Django |
| PostgreSQL | 14+ | Base de datos del servidor central |
| Git | — | Control de versiones |
| Node.js | 20+ (LTS) | Frontend SPA en `frontend/` |

## Pasos para iniciar en tu máquina local

### 1. Clonar el repositorio y situarse en la rama `develop`

```bash
git clone https://github.com/Enrrill/DLL-Sulimados---Core.git
cd DLL-Sulimados---Core
git checkout develop
git pull origin develop
```

### 2. Crear el entorno virtual (venv)

```bash
# En la raíz del proyecto:
python -m venv venv
```

### 3. Activar el entorno virtual

- En **Windows (PowerShell):**

  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

- En **Windows (CMD):**

  ```cmd
  .\venv\Scripts\activate.bat
  ```

- En **Linux / macOS:**

  ```bash
  source venv/bin/activate
  ```

### 4. Instalar las dependencias encapsuladas

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 5. Configurar las variables de entorno

Copiar el archivo de ejemplo `.env.example` a `.env` en la raíz y ajustar los valores:

- En **Windows (PowerShell):**

  ```powershell
  Copy-Item .env.example .env
  ```

- En **Linux / macOS:**

  ```bash
  cp .env.example .env
  ```

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `SECRET_KEY` | Clave secreta de Django. **Obligatoria y distinta en cada ambiente.** | — |
| `DEBUG` | Modo depuración | `True` en desarrollo |
| `ALLOWED_HOSTS` | Hosts servidos, separados por comas | `localhost,127.0.0.1` |
| `DB_ENGINE` | Motor de base de datos | `django.db.backends.postgresql` |
| `DB_NAME` | Nombre de la base de datos | `dll_sublimados` |
| `DB_USER` / `DB_PASSWORD` | Credenciales de la base de datos | `postgres` / `tu_contrasena_segura` |
| `DB_HOST` / `DB_PORT` | Servidor de base de datos | `localhost` / `5432` |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para la SPA | `http://localhost:5173,http://127.0.0.1:5173` |
| `TASA_CAMBIO_DEFAULT` | Tipo de cambio USD → Bs inicial | `36.50` |

> ⚠️ `.env` está en `.gitignore`. Nunca se versiona; se versiona solo `.env.example`.

### 6. Base de datos, migraciones y datos iniciales

```bash
# 1. Crear base de datos local (opcional si no usas Neon, ver database/00_crear_bd.sql):
psql -U postgres -f database/00_crear_bd.sql

# 2. Aplicar migraciones limpias (en Neon usar DATABASE_URL=$DATABASE_URL_UNPOOLED):
python manage.py migrate

# 3. Crear superusuario administrador:
python manage.py createsuperuser

# 4. Cargar seeders iniciales en orden de dependencias:
psql "$DATABASE_URL" -f database/seeders/01_seed_nucleo.sql
psql "$DATABASE_URL" -f database/seeders/02_seed_catalogo_inventario.sql
psql "$DATABASE_URL" -f database/seeders/03_seed_compras_produccion.sql
psql "$DATABASE_URL" -f database/seeders/04_seed_ventas_precios_rrhh.sql

# 5. Iniciar servidor backend:
python manage.py runserver
```

### 7. Poner en marcha el frontend (SPA)

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

La aplicación web estará accesible en `http://localhost:5173`, con proxy automático de `/api` hacia `http://localhost:8000`.

## Comandos habituales

| Comando | Para qué |
| --- | --- |
| `python manage.py makemigrations <app>` | Generar las migraciones de una app |
| `python manage.py migrate` | Aplicar las migraciones |
| `python manage.py createsuperuser` | Crear el usuario administrador inicial |
| `python manage.py runserver` | Levantar el servidor de desarrollo |
| `pytest` | Ejecutar la suite de pruebas unitarias |
| `flake8 backend/` | Verificar cumplimiento de PEP 8 y estilo |
| `black --check backend/` | Comprobar formateo de código |
| `cd frontend && npm run dev` | Iniciar servidor de desarrollo Vite |
| `cd frontend && npm run build` | Compilar frontend para producción |

## Estructura del repositorio

```text
DLL-Sulimados---Core/
├── manage.py                # Punto de entrada Django en la raíz (estándar OptiRosse)
├── requirements.txt         # Dependencias del backend
├── requirements-dev.txt     # Dependencias de desarrollo
├── .env.example             # Plantilla de variables de entorno
├── pyproject.toml           # Configuración de black, isort y pytest
├── database/                # Scripts SQL de arranque y datos iniciales
├── backend/                 # Backend modular Django
│   ├── config/              # settings, urls de la API, asgi/wsgi
│   ├── common/              # base_models y utilidades compartidas
│   └── apps/                # Aplicaciones modulares (core, catalog, inventory...)
├── frontend/                # SPA React + Vite + Tailwind CSS
│   ├── src/                 # features/, app/, components/, services/
│   ├── package.json
│   └── vite.config.js
├── docs/                    # Documentación técnica completa
└── tests/                   # Pruebas de integración
```

El backend vive en `backend/` con `manage.py` en la raíz (idéntico al estándar de `OptiRosse`) y expone la API REST bajo el prefijo `/api/v1/`. Los modelos de negocio de cada app los diseña e implementa el **Grupo de Base de Datos**, exigiendo en cada uno el uso explícito de `class Meta` con `db_table`. La SPA en React + Vite + Tailwind vive en `frontend/` y se conecta al backend por proxy en `/api/`.

Los equipos trabajan con ramas `feature/*` derivadas de `develop`; el flujo completo está en [10 Git Flow y normas del equipo](10-git-flow-y-normas-del-equipo.md) y las normas de commits en [14 Convenciones de commits](14-convenciones-de-commits.md).

## Ambientes

| Ambiente | Propósito | Notas |
| --- | --- | --- |
| `dev` | Desarrollo local | PostgreSQL local o SQLite para pruebas rápidas |
| `staging` | Pruebas de integración | Opcional |
| `prod` | Servidor central | Credenciales y `SECRET_KEY` propias, `DEBUG=False` |

El backup diario del servidor central es `pg_dump` comprimido con retención de 30 días (RNF-06).

## Licencia

Este proyecto es de carácter académico y está destinado al uso exclusivo en la evaluación de la materia **Lenguajes de Programación III**.

## Referencias

- [11 Normas de código y POO](11-normas-de-codigo-y-poo.md)
- [10 Git Flow y normas del equipo](10-git-flow-y-normas-del-equipo.md)
- [14 Convenciones de commits](14-convenciones-de-commits.md)
- [04 Arquitectura del monolito modular](04-arquitectura-del-monolito-modular.md)
- [07 Convenciones de base de datos](07-convenciones-de-base-de-datos.md)
- [Glosario](referencias/glosario-del-negocio.md)
