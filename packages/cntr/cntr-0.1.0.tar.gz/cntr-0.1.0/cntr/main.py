import logging
from os import path
from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, Response, StreamingResponse
from starlette.staticfiles import StaticFiles
from cntr.api import api_router
from cntr.config import settings
from cntr.database import SessionLocal
from tabulate import tabulate
import httpx

# from starlette.middleware.cors import CORSMiddleware

log = logging.getLogger(__name__)

# we create the ASGI for the app
app = Starlette()

# we create the ASGI for the frontend
frontend = Starlette()

# we create the Web API framework
# app = FastAPI(
#     title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )
api = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@frontend.middleware("http")
async def default_page(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        if settings.STATIC_DIR:
            return FileResponse(path.join(settings.STATIC_DIR, "index.html"))
        else:
            async with httpx.AsyncClient() as client:
                remote_resp = await client.get(
                    str(request.url.replace(port=8080)), headers=dict(request.headers)
                )
                return StreamingResponse(
                    remote_resp.aiter_bytes(),
                    headers=remote_resp.headers,
                    status_code=remote_resp.status_code,
                    media_type=remote_resp.headers.get("content-type"),
                )
    return response


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal Server Error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=31536000 ; includeSubDomains"
    return response


# # Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

api.include_router(api_router, prefix="/v1")

# we mount the frontend and app
if settings.STATIC_DIR:
    frontend.mount("/", StaticFiles(directory=settings.STATIC_DIR), name="app")


app.mount("/api", app=api)
app.mount("/", app=frontend)

# we print all the registered API routes to the console
table = []
for r in api_router.routes:
    auth = any(
        d.dependency.__name__ == "get_current_user" for d in r.dependencies
    )  # TODO this is fragile
    table.append([r.path, auth, ",".join(r.methods)])

log.debug(
    "Available Endpoints \n"
    + tabulate(table, headers=["Path", "Authenticated", "Methods"])
)
