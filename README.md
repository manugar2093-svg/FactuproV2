# FactuPro — Deployment en Render

## Estructura del proyecto

```
factupro/
├── main.py              ← Entry point (este archivo)
├── requirements.txt
├── render.yaml          ← Config de Render
├── .env.example
├── static/
│   └── index.html       ← Frontend SPA
└── (tu backend existente: routers/, models/, db.py, etc.)
```

## Paso 1 — Integrar este main.py con tu backend

Edita `main.py` y ajusta el import del router:

```python
# Ejemplo si tu estructura es:
from routers import router as api_router   # routers/__init__.py
# o si tienes múltiples routers:
from routers.facturas import router as facturas_router
from routers.clientes import router as clientes_router
# etc.
```

Todos los endpoints del API deben quedar bajo el prefijo `/api`:
- `POST /api/auth/login`
- `GET  /api/clientes`
- `GET  /api/facturas`
- etc.

## Paso 2 — Agregar endpoint de salud (health check)

En cualquier router, agrega:

```python
@router.get("/health")
def health():
    return {"status": "ok"}
```

Render lo usa para saber si el servicio arrancó correctamente.

## Paso 3 — Subir a GitHub

```bash
git init
git add .
git commit -m "feat: factupro web deploy"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/factupro.git
git push -u origin main
```

## Paso 4 — Deploy en Render

1. Ve a https://dashboard.render.com/web/new
2. Conecta tu repositorio de GitHub
3. Render detecta el `render.yaml` automáticamente
4. En **Environment Variables**, agrega:
   - `DATABASE_URL` = tu cadena de conexión MySQL externa
5. Click en **Deploy**

## Base de datos MySQL en la nube (opciones gratuitas)

| Opción | Plan gratis | Notas |
|--------|-------------|-------|
| **Railway** | $5 crédito/mes | MySQL nativo, fácil |
| **PlanetScale** | 5 GB gratis | MySQL-compatible |
| **Filess.io** | Básico gratis | Hosting RD |

### Cadena de conexión Railway:
```
mysql+pymysql://root:PASSWORD@HOST:PORT/railway
```

## Probar localmente

```bash
pip install -r requirements.txt
cp .env.example .env   # editar con tus datos
uvicorn main:app --reload
# Abrir: http://localhost:8000
```
