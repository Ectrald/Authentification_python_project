from fastapi import APIRouter, FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.routers import auth, users

app = FastAPI()

register_exception_handlers(app)

router = APIRouter()
router.include_router(users.router)
router.include_router(auth.router)
app.include_router(router)