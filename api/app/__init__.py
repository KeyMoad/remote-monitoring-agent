from logging import getLogger
from fastapi import FastAPI, Request, status as fastApiStatus
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from app.routers import auth_route, cronjob_route,services_route, metrics_route
from app.settings import *
from app.utils import *

app = FastAPI(
    version="1.0.0",
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    summary=APP_SUMMARY,
    docs_url=None,
    redoc_url=None,
    license_info=LICENSE_INFO
)

logger = getLogger('uvicorn.error')

# Add middleware
app.add_middleware(
    GZipMiddleware,
    minimum_size=100
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router=auth_route.router, tags=["Auth"])
app.include_router(router=cronjob_route.router, tags=["CronJob"])
app.include_router(router=services_route.router, tags=["Services"])
app.include_router(router=metrics_route.router, tags=["Metrics"])


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = {}
    for error in exc.errors():
        details[error["loc"][-1]] = error.get("msg")
    return JSONResponse(
        status_code=fastApiStatus.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": details}),
    )
