# DLL Sublimados — Core

Monorepo de gestión para negocio de sublimación, confección y planchado (3 locales).
Stack: Django 6.1 + PostgreSQL 14+ (Neon) + React 19 + JavaScript + Vite + Tailwind CSS v4.

---

## 🏗️ Arquitectura del Repositorio

- `manage.py`: En la raíz del repositorio (estándar Django).
- `backend/`: Código fuente de la API REST Django.
  - `config/`: Configuración del proyecto (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
  - `common/`: Clases base abstractas y utilidades compartidas (`base_models.py`).
  - `apps/`: Apps modulares (`core`, `catalog`, `inventory`, `purchasing`, `production`, `sales`, `pricing`, `hr`, `documents`, `reports`, `audit`).
- `frontend/`: SPA en React 19 + Vite + Tailwind CSS v4.
- `database/`: Scripts SQL puros de arranque y datos iniciales (mantenido por el Grupo de Base de Datos).
- `docs/`: Vault de documentación técnica (Markdown con diagramas Mermaid).
- `neon.ts`: Configuración de Neon (política de branches, servicios habilitados).
- `package.json`: Dependencias de configuración de Neon (`@neon/config`, `@neon/env`) usadas por `neon.ts`.

---

## 🐍 Backend (Django)

- **Settings:** `backend/config/settings.py` (`DJANGO_SETTINGS_MODULE=backend.config.settings`).
- **Variables de entorno:** Archivo `.env` en la raíz del proyecto (cargado automáticamente con ruta absoluta). Ver `.env.example` para la lista completa de variables requeridas.
- **Base de datos:** PostgreSQL 14+ en Neon (Lakebase Postgres serverless). La conexión se configura via `DATABASE_URL` (pooler PgBouncer, para la app) y `DATABASE_URL_UNPOOLED` (endpoint directo, solo para migraciones). Ver `docs/neon.md`.
- **Registro de apps:** En `INSTALLED_APPS` se registran como `'backend.apps.<nombre>'`.
- **Modelo de Usuario:** `core.Usuario` fijado en `AUTH_USER_MODEL = 'core.Usuario'`:
  - Hereda de `AbstractBaseUser`, `PermissionsMixin`, `TimeStampedModel` y `ActivoMixin`.
  - `USERNAME_FIELD = 'nombre_usuario'`, `REQUIRED_FIELDS = ['correo']`.
  - Roles: `admin`, `gerente`, `operario`, `vendedor`.
  - Soporte de multi-local con FK a `Local` y bandera booleana `es_global`.
- **Modelos base:** `backend/common/base_models.py`:
  - `TimeStampedModel`: agrega `creado_en` y `actualizado_en`.
  - `ActivoMixin`: borrado lógico con `activo = models.BooleanField(default=True)`.
- **REGLA OBLIGATORIA DE MODELOS:**
  - Todo modelo diseñado e implementado debe definir explícitamente `class Meta:` con su `db_table` correspondiente (ej. `db_table = 'locales'`), además de `verbose_name` y `verbose_name_plural` en español.
  - Las entidades de negocio se modelan en español; los identificadores de código (servicios, vistas) en inglés.
- **Capa de Servicios:** La lógica de negocio reside estrictamente en `services.py` de cada app; las vistas (`views.py`) y serializadores (`serializers.py`) son delgados.
- **API REST:** Prefijo global `/api/v1/`, con enrutamiento modular por app.

---

## ⚛️ Frontend (React + Vite)

- **Herramientas:** React 19 + JavaScript + Vite + Tailwind CSS v4.
- **Estilos:** Tailwind v4 configurado con `@tailwindcss/vite` e `@import "tailwindcss";` en `src/index.css`.
- **Proxy de desarrollo:** `vite.config.js` redirige `/api` automáticamente hacia `http://localhost:8000`.
- **Gestor de paquetes:** `npm` con scripts `npm run dev` y `npm run build`.

---

## 👥 Responsabilidad de Equipos (Normativa)

1. **Grupo de Base de Datos:** Dueño exclusivo del diseño relacional, DDL en `database/` y de implementar los modelos en `backend/apps/<app>/models.py` (con `class Meta.db_table`).
2. **Grupo de Backend:** Lógica de negocio en `services.py`, controladores de API (`views.py`, `serializers.py`, `urls.py`) y tests unitarios.
3. **Grupo de Frontend:** Interfaz de usuario en `frontend/` consumiendo los endpoints de la API.
4. **Grupo de Gestión:** Administración del repositorio, revisión de PRs, supervisión de Git Flow y CI/CD.

---

## 🌿 Convenciones de Commits (Conventional Commits)

Todo commit debe incluir título en imperativo y desglose explícito de cambios:

```text
<tipo>(<ámbito>): <título en imperativo, minúscula, sin punto final>

- <descripción detallada del cambio 1>
- <descripción detallada del cambio 2>

Refs: RF-XX
```

- **Tipos válidos:** `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `style`, `build`, `ci`, `chore`, `revert`.
- **Ámbitos válidos:** Apps de backend (`core`, `catalog`, `inventory`, `purchasing`, `production`, `sales`, `pricing`, `hr`, `documents`, `reports`, `audit`), `frontend`, `docs`, `deps`, `config`.

---

## ⚡ Comandos Rápidos

```bash
# Entorno virtual y backend
source venv/bin/activate
python manage.py check
python manage.py migrate
python manage.py runserver

# Migraciones contra Neon (endpoint directo, sin pooler)
DATABASE_URL=$DATABASE_URL_UNPOOLED python manage.py migrate

# Calidad y pruebas
flake8 backend/ manage.py
pytest

# Frontend
cd frontend
npm run dev
npm run build
```

