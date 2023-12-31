from fastapi import APIRouter
from api.logs import router as logs_router

router = APIRouter()

router.include_router(logs_router, prefix="/logs", tags=["Log Endpoints"])
