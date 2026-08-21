from fastapi import FastAPI
from backend.app.api.v1.endpoints import items, inventory, auth
from backend.app.db.database import init_db, close_db

app = FastAPI(title="DavoraInventario API", version="0.1.0")

# Incluir routers
app.include_router(items.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    # Inicializa tablas y vistas a partir de Schema.sql (si es necesario)
    try:
        await init_db()
    except Exception as e:
        # No abortamos; mostrar advertencia para debugging
        print("Warning: init_db fallo:", e)

@app.on_event("shutdown")
async def on_shutdown():
    try:
        await close_db()
    except Exception as e:
        print("Warning: close_db fallo:", e)
