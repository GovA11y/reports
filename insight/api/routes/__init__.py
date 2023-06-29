# __init__.py
# Relative Path: insight/api/routes/__init__.py
from fastapi import APIRouter
from .metrics import router as metrics_router
from .issues import router as issues_router

router = APIRouter()

router.include_router(metrics_router, prefix="/metrics")

# Issues Endpoint
router.include_router(issues_router, prefix="/issues")

# adding a new router, for example:
# from .new_module import router as new_module_router
# router.include_router(new_module_router, prefix="/new_module")