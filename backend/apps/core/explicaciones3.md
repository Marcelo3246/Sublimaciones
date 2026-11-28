# Pruebas y cambios del flujo de login

En este documento se describen las pruebas realizadas sobre los cambios del
login, la renovación y revocación de tokens, el perfil del usuario y los
permisos que determinan qué información puede consultar cada usuario.

## Archivos revisados o modificados

| Archivo | Cambio |
| --- | --- |
| `backend/apps/core/tests.py` | Se ampliaron las pruebas automatizadas de autenticación y permisos. |
| `backend/apps/core/views.py` | Se corrigió el filtrado de locales para usuarios globales y usuarios sin local asignado. |
| `backend/apps/core/urls.py` | Se eliminó una ruta de logout duplicada y mal formada. |
| `backend/config/urls.py` | Se verificó que conserva la ruta pública correcta de logout. No fue necesario modificarlo. |

## Ajuste del acceso a locales

`LocalViewSet.get_queryset()` limita los resultados de
`GET /api/v1/core/locales/` de acuerdo con el alcance del usuario:

| Usuario autenticado | Locales que puede consultar |
| --- | --- |
| Administrador | Todos los locales activos. |
| Usuario global (`es_global=True`) | Todos los locales activos. |
| Usuario con local asignado | Solo el local asignado. |
| Usuario sin local asignado y que no es global | Ninguno. |

Antes del ajuste, el usuario no administrador que no tuviera un local asignado
recibía la consulta sin filtrar y podía ver todos los locales. Ahora la vista
devuelve una consulta vacía para ese caso. El permiso `AccesoLocal` sigue
determinando si el usuario puede acceder a la operación; este filtrado
determina qué registros puede ver.

## Ruta de cierre de sesión

La ruta correcta está registrada en `backend/config/urls.py`:

```text
POST /api/v1/auth/token/logout/
```

La vista `TokenBlacklistView` recibe un JSON con el refresh token:

```json
{
  "refresh": "<refresh_token>"
}
```

Si el token es válido, Simple JWT lo agrega a la lista negra y ya no permite
usarlo para obtener otro access token. El access token ya emitido puede seguir
siendo válido hasta su vencimiento.

En `backend/apps/core/urls.py` había otra declaración de logout que, al estar
incluida bajo `/api/v1/core/`, creaba una ruta redundante y mal formada:
`/api/v1/core/api/v1/auth/token/logout/`. Se eliminó esa declaración y sus
imports, dejando una sola ruta pública y evitando el prefijo duplicado.

## Cobertura de las pruebas

La clase `CoreModelsTest` ya verificaba la creación de modelos, el login
correcto y el rechazo de una contraseña incorrecta. La cobertura total incluye
los siguientes comportamientos:

| Prueba | Comportamiento esperado |
| --- | --- |
| Login correcto | Devuelve los tokens `access` y `refresh`. |
| Contraseña incorrecta | Rechaza las credenciales con HTTP 401. |
| Renovación de token | Devuelve un nuevo access y rota el refresh token. |
| Reutilización del refresh anterior | Rechaza el token anterior con HTTP 401. |
| Logout | Revoca el refresh token; un intento posterior de renovarlo devuelve HTTP 401. |
| Perfil sin token | `GET /api/v1/core/perfil/` devuelve HTTP 401. |
| Perfil con access token | Devuelve HTTP 200 y los datos del usuario autenticado. |
| Usuario sin local | Obtiene una lista vacía de locales. |
| Usuario con local asignado | Solo obtiene el local asignado. |
| Usuario global | Puede consultar todos los locales activos. |
| Listado de usuarios | Rechaza a un usuario normal con HTTP 403 y permite el acceso al administrador. |

Las pruebas existentes de creación de usuario, local, tasa de cambio y
contador correlativo también forman parte de `backend.apps.core.tests`.

## Ejecución y resultados

### Comprobación del proyecto

Se ejecutó:

```powershell
python manage.py check
```

Resultado: `System check identified no issues (0 silenced)`.

También se compiló el código Python del módulo:

```powershell
python -m compileall -q backend\apps\core
```

La compilación terminó correctamente.

### Pruebas automatizadas del módulo core

La ejecución habitual:

```powershell
python manage.py test backend.apps.core.tests -v 2
```

no pudo crear la base de pruebas porque PostgreSQL no estaba disponible en
`localhost:5432` (conexión rechazada).

Se intentó usar SQLite, que está contemplado por la configuración local. Sin
embargo, las migraciones incluyen SQL específico de PostgreSQL: la migración
`audit.0002_alter_bitacoraaccion_table_alter_bitacorastock_table` intenta
ejecutar una instrucción `CREATE SCHEMA`, que SQLite no admite. Por ello, las
pruebas se ejecutaron con una base SQLite en memoria y con las migraciones
deshabilitadas únicamente durante ese proceso. Django creó las tablas a partir
de los modelos para poder comprobar el comportamiento de las vistas y los
tokens.

Resultado: **12 pruebas ejecutadas, 12 aprobadas**.

La salida mostró advertencias no bloqueantes de DRF porque los querysets de
usuarios y locales no tienen un orden explícito al paginar. No causaron fallos
y no se modificó el orden de esos endpoints como parte de este trabajo.

> La ejecución con SQLite sin migraciones valida el comportamiento de las
> pruebas, pero no sustituye la validación de las migraciones reales en
> PostgreSQL. Cuando PostgreSQL esté disponible, conviene ejecutar de nuevo
> `python manage.py test backend.apps.core.tests -v 2` con la configuración
> normal del proyecto.

## Resumen

El resultado cubre el ciclo de autenticación: emitir tokens al iniciar sesión,
renovarlos, impedir su reutilización luego de la rotación, revocarlos al cerrar
sesión y proteger el perfil. También verifica la autorización por rol y el
alcance por local. Las 12 pruebas del módulo pasaron en SQLite en memoria y el
chequeo de configuración de Django no encontró problemas; queda pendiente
repetir las pruebas con las migraciones reales cuando PostgreSQL esté activo.