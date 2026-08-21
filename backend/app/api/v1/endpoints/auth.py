from fastapi import APIRouter

router = APIRouter(tags=["auth"], prefix="/auth")

# Endpoints mínimos: ampliar con seguridad (JWT) si lo deseas
@router.get("/ping")
async def ping():
    return {"msg": "auth pong"}
