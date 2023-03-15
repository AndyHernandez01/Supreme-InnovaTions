from fastapi import FastAPI

from app.api.api1 import api_router
from app.config import settings


app = FastAPI(
        title="wds_api", openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
