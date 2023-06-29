# __init__.py
# Relative Path: insight/api/routes/__init__.py
from fastapi import APIRouter
from .metrics import router as metrics_router

router = APIRouter()

router.include_router(metrics_router, prefix="/metrics")

# adding a new router, for example:
# from .new_module import router as new_module_router
# router.include_router(new_module_router, prefix="/new_module")