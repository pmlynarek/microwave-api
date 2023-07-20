from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer

from app.api.endpoints import health
from app.api.endpoints import microwave

# This dependency is added so that "Authorize" button appears in swagger documentation.
# Bearer token can be pasted there and all requests will use it in test requests
bearer = HTTPBearer(auto_error=False)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(microwave.router, tags=["microwave"], dependencies=[Depends(bearer)])
