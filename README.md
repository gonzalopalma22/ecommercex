# eCommerce-X — Backend

API REST desarrollada con Django y Django REST Framework para la gestión de productos, pedidos y autenticación de usuarios. Incluye scraping automático de productos desde [okwu.cl](https://okwu.cl).

## Tecnologías

- Python 3.10+
- Django 5.2
- Django REST Framework
- Django REST Framework SimpleJWT
- Django CORS Headers
- SQLite (desarrollo)

## Arquitectura

Se implementó una arquitectura **monolítica modular**, donde cada dominio está desacoplado en su propia app Django con modelos, vistas y URLs independientes, siguiendo el patrón **Repository + Service Layer**.

```
ecommercex/
├── inventario/       # Scraping + gestión de productos
├── pedidos/          # CRUD de pedidos
├── autenticacion/    # Autenticación JWT
└── ecommercex/       # Configuración global
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/gonzalopalma22/ecommercex.git
cd ecommercex
```

### 2. Instalar dependencias

```bash
pip install django djangorestframework djangorestframework-simplejwt requests django-cors-headers
```

### 3. Migrar la base de datos

```bash
python manage.py migrate
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
```

### 5. Levantar el servidor

```bash
python manage.py runserver
```

El servidor queda disponible en `http://127.0.0.1:8000`

---

## Endpoints

### Autenticación

| Método | URL | Descripción | Auth |
|--------|-----|-------------|------|
| `POST` | `/api/auth/login/` | Obtener token JWT | No |
| `POST` | `/api/auth/refresh/` | Refrescar token | No |

**Body login:**
```json
{
    "username": "admin",
    "password": "tu_contraseña"
}
```

**Respuesta:**
```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

---

### Productos (Scraping)

| Método | URL | Descripción | Auth |
|--------|-----|-------------|------|
| `GET` | `/api/productos/` | Listar productos desde BD | No |
| `POST` | `/api/productos/actualizar/` | Ejecutar scraping desde okwu.cl | No |

**Respuesta productos:**
```json
[
    {
        "id": 1,
        "nombre": "Magic Lipstick",
        "precio_regular": "19990.00",
        "precio_oferta": null,
        "variantes": "Default Title",
        "url_imagen": "https://cdn.shopify.com/...",
        "disponible": true
    }
]
```

---

### Pedidos

| Método | URL | Descripción | Auth |
|--------|-----|-------------|------|
| `GET` | `/api/pedidos/` | Listar pedidos | ✅ JWT |
| `POST` | `/api/pedidos/` | Crear pedido | ✅ JWT |
| `PUT` | `/api/pedidos/{id}/` | Editar pedido | ✅ JWT |
| `DELETE` | `/api/pedidos/{id}/` | Eliminar pedido | ✅ JWT |

**Body crear pedido:**
```json
{
    "cliente": "Juan Pérez",
    "producto": "Magic Lipstick",
    "cantidad": 2,
    "estado": "PENDIENTE"
}
```

**Estados disponibles:** `PENDIENTE`, `PROCESADO`, `ENVIADO`

---

## Autenticación con JWT

Para endpoints protegidos, incluir el token en el header:

```
Authorization: Bearer eyJ...
```

---

## Patrón de diseño

Se aplicó el patrón **Repository + Service Layer**:

- **Model** (`models.py`) — Define la estructura de datos
- **Service** (`scraping.py`) — Lógica de negocio separada de la vista
- **Repository** — ORM de Django para acceso a la BD
- **View** (`views.py`) — Solo recibe la request y devuelve la response

Esto garantiza que si la fuente externa okwu.cl cambia, solo se modifica `scraping.py` sin afectar el resto del sistema.

---

## Manejo de errores en scraping

Si okwu.cl no está disponible, el sistema retorna los productos almacenados en la base de datos sin interrumpir el servicio.

---

## Frontend

El frontend desarrollado en React + Vite se encuentra en el repositorio del compañero de equipo y se conecta a esta API mediante la URL base `http://127.0.0.1:8000/api`.
