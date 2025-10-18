# Profile

A small Django project using Django REST Framework (DRF). This README covers setup on Windows PowerShell, environment variables, migrations, running the dev server, useful endpoints, troubleshooting, and how to add Swagger/OpenAPI documentation.

---

## Prerequisites

- Python 3.8+ (use the same version as the provided virtualenv if you want to reuse it)
- PowerShell (Windows)

The repository includes a virtual environment at `hng-env/`. You can either use it or create a new one.

## Quick setup (PowerShell)

1. Activate the included virtualenv (PowerShell):

```powershell
# If you want to use the provided venv
.\hng-env\Scripts\Activate
```

2. (Optional) Create a new venv and install dependencies:

```powershell
python -m venv .venv
venv\Scripts\Activate
pip install -r requirements.txt
```

3. Set environment variables for the current session (example):

```powershell
# Example: used by the ProfileView
$env:My_EMAIL = 'you@example.com'
```

To set it permanently for your Windows user:

```powershell
[Environment]::SetEnvironmentVariable('My_EMAIL','you@example.com','User')
```

4. Apply database migrations (creates built-in tables such as `django_session`):

```powershell
python manage.py migrate
```

5. Run the development server:

```powershell
python manage.py runserver
```

6. Open the example endpoint in your browser:

http://127.0.0.1:8000/me

---

## Default settings and environment variables used

- `My_EMAIL` — used by `ProfileView` to populate the returned `email` field. The project has a default value in `hng_api/settings.py` but it's recommended to set your own for development.

Other settings like `EXTERNAL_API_URL` and `EXTERNAL_API_TIMEOUT` are defined in `hng_api/settings.py`.

---

## Endpoints (example)

- GET /me — returns the profile data combined with a cat fact fetched from an external API.

(Adjust URLs if you have configured a different `ROOT_URLCONF` or path prefix.)

---

## Troubleshooting

- TemplateDoesNotExist: rest_framework/api.html
  - Ensure `rest_framework` is listed in `INSTALLED_APPS` in `hng_api/settings.py`.
  - Ensure `APP_DIRS = True` in your TEMPLATES setting so app templates are discovered.
  - Run `python manage.py migrate` and restart the dev server.

- OperationalError: no such table: django_session
  - Run `python manage.py migrate` to create the sessions and other built-in tables.

- AttributeError: module 'datetime' has no attribute 'now'
  - Import datetime properly in views: `from datetime import datetime, timezone`, then use `datetime.now(timezone.utc)`.

If an error persists, copy the traceback from the server console and inspect the file/line referenced.

---

## Adding Swagger / OpenAPI documentation

This project doesn't ship a built-in Swagger UI by default. The recommended approach is to use `drf-spectacular`. Below are the steps to add an interactive Swagger UI.

Recommended: drf-spectacular

1. Install:

```powershell
pip install drf-spectacular
```

2. Update `hng_api/settings.py`:

```python
# settings.py
INSTALLED_APPS += [
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

3. Add routes to `hng_api/urls.py`:

```python
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # your existing routes
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

4. Run the server and visit the UI:

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

Alternative: drf-yasg

- Install `drf-yasg` and follow its README to wire up schema and UI views (common endpoints are `/swagger/` and `/redoc/`).

Notes

- After installing packages, restart the dev server.
- If your API is behind a path prefix, adjust the example routes accordingly.

---

## Running checks

Quick Django system check:

```powershell
python manage.py check
```

Generate requirements (if you need one):

```powershell
pip freeze > requirements.txt
```

---

## Contact / Author

Project created for a tutorial/exercise. Adjust settings and environment variables before deploying to production.
