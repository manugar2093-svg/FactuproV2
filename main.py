"""
FactuPro - Web Entry Point
Sirve el frontend (index.html) y monta el API en /api
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# ─── Importa tu router principal del backend existente ───────────────────────
# Ajusta el import según la estructura de tu proyecto:
#   from app.api import router as api_router          # si usas app/api/__init__.py
#   from routers import router as api_router          # si tienes routers.py
#   from api import app as api_router                 # etc.
#
# Por ahora dejamos un placeholder que puedes conectar:
from api import router as api_router   # ← AJUSTA ESTE IMPORT

app = FastAPI(title="FactuPro", version="2.0")

# ─── CORS (necesario si frontend y backend corren en dominios distintos) ──────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en producción: restringe a tu dominio de Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Monta el API en /api ─────────────────────────────────────────────────────
app.include_router(api_router, prefix="/api")

# ─── Sirve archivos estáticos (CSS, JS, imágenes si los tienes) ───────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ─── Sirve el index.html en la raíz y cualquier ruta desconocida ─────────────
@app.get("/", include_in_schema=False)
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa(full_path: str = ""):
    # Rutas que empiezan con /api no deben llegar aquí (FastAPI las maneja primero)
    index_file = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_file, media_type="text/html")
