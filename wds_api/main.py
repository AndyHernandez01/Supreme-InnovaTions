from fastapi import FastAPI

from api.api1 import api_router
from config import settings
import uvicorn


if __name__ == "__main__":
  uvicorn.run("main:app", port=8000, log_level="info")

app = FastAPI(
        title="wds_api", openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
