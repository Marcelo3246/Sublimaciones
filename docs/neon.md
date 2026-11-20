# Neon — Base de Datos en la Nube

> Lakebase Postgres serverless. DLL Sublimados usa Neon como base de datos de producción.

## Proyecto

| Campo | Valor |
|---|---|
| Nombre | `dll-sublimados` |
| ID | `falling-firefly-71986564` |
| Organización | `org-sparkling-union-44915996` |
| Región | `aws-sa-east-1` (São Paulo) |
| Consola | <https://console.neon.tech/app/projects/falling-firefly-71986564/> |

---

## Conexión

Neon expone **dos endpoints** por branch:

| Variable | Endpoint | Cuándo usarla |
|---|---|---|
| `DATABASE_URL` | Pooler PgBouncer (puerto 5432) | App Django en todo momento |
| `DATABASE_URL_UNPOOLED` | Endpoint directo | Solo para `migrate`, `dbshell`, y herramientas que abren transacciones largas |

### ¿Por qué dos endpoints?

PgBouncer opera en modo **transaccional**: descarta el estado de sesión entre transacciones.
Algunas operaciones de Django (migraciones, `SELECT FOR UPDATE`, advisory locks) requieren
estado de sesión persistente y deben ir por el endpoint directo.

---

## Integración en Django

`settings.py` prioriza `DATABASE_URL` si está definida:

```python
# Prioridad: DATABASE_URL > SQLite (debug) > vars DB_* (local)
if os.environ.get("DATABASE_URL"):
    DATABASES = {"default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,        # keep-alive al pooler
        conn_health_checks=True,
        ssl_require=True,
    )}
```

`dj-database-url` traduce la URL completa (incluido `sslmode` y `channel_binding`) al dict
que Django espera en `DATABASES`.

---

## Variables de entorno

Inyectadas automáticamente por `neon init`. Ver también [`.env.example`](../.env.example).

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | URL completa al pooler (app Django) |
| `DATABASE_URL_UNPOOLED` | URL al endpoint directo (migraciones) |
| `NEON_BRANCH` | Nombre de la branch activa (ej. `production`) |
| `NEON_BRANCH_ID` | ID interno de la branch |
| `NEON_FUNCTION_HOST_SUFFIX` | Sufijo para Neon Functions |

Para obtener nuevas credenciales al cambiar de branch:

```bash
neon checkout <nombre-branch>
```

---

## Branches de base de datos

Neon soporta branches igual que Git: cada branch es un snapshot de los datos en ese instante.

```
production  ←── branch principal (siempre activa)
    └── dev      ←── branch personal de desarrollo (expira en 7 días)
    └── feature  ←── branch por feature/PR
```

Configuración de TTL en [`neon.ts`](../neon.ts): las branches no-default expiran a los **7 días**.

### Crear una branch de desarrollo

```bash
neon checkout dev --create      # crea branch "dev" y actualiza .env
python manage.py migrate        # aplica migraciones en la branch
```

### Volver a producción

```bash
neon checkout production
```

---

## Migraciones

Siempre usar el endpoint **directo** para migraciones (evita conflictos con el pooler transaccional):

```bash
# Opción A: variable inline
DATABASE_URL=$DATABASE_URL_UNPOOLED python manage.py migrate

# Opción B: en scripts CI/CD, exportar antes
export DATABASE_URL=$DATABASE_URL_UNPOOLED
python manage.py migrate
```

---

## Comandos útiles de la CLI

```bash
neon --version                   # versión instalada
neon branches list               # listar branches del proyecto
neon checkout dev --create       # crear branch de desarrollo
neon checkout production         # volver a producción
neon config plan                 # previsualizar cambios de neon.ts
neon deploy                      # aplicar cambios de neon.ts al proyecto
neon api-keys list               # ver API keys activas
```

> La CLI está instalada en `~/.local/bin/neon`. Si no está en el PATH, agregar
> `export PATH="$HOME/.local/bin:$PATH"` al shell profile.

---

## Archivo `neon.ts`

Ubicado en la raíz del repositorio. Define la política de branches:

```typescript
export default defineConfig({
  auth: false,            // Neon Auth no utilizado (usamos JWT propio)
  branch: (branch) => {
    if (branch.isDefault) return {};         // producción: sin cambios automáticos
    if (!branch.exists) return { ttl: "7d" }; // branches nuevas: expiran en 7 días
    return {};
  },
});
```

---

## Responsabilidades por grupo

| Grupo | Tarea relacionada con Neon |
|---|---|
| **Base de Datos** | Migraciones (`migrate`), diseño de schema, branches de BD |
| **Backend** | Conexión Django (`DATABASE_URL`), queries, servicios |
| **Gestión** | Rotación de API keys, monitoreo de consola Neon, CI/CD |

