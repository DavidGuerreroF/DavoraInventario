# Dependencias reutilizables para rutas (get_db alias)
from typing import AsyncGenerator
from backend.app.db.database import get_db as get_db_session

# FastAPI puede usar directamente get_db_session; exporto un alias claro
async def get_db() -> AsyncGenerator:
    async for session in get_db_session():
        yield session
