'''API file'''

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import settings

from src.api.api_v1 import endpoints as endpoints_v1

app = FastAPI(title=settings.PROJECT_NAME)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(endpoints_v1.listing_router, prefix=settings.API_V1_STR)
app.include_router(endpoints_v1.generation_router, prefix=settings.API_V1_STR)
