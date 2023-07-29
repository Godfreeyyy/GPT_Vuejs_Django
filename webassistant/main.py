from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from api_server.router import open_ai_router
from fastapi.middleware.cors import CORSMiddleware


def init_app() -> FastAPI:
    _app = FastAPI(title="CMS API", version="0.2.0")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins="*",  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    _app.include_router(open_ai_router.OpenAIRouter().add_routesDr().router, prefix="/open-ai", tags=["project"])

    return _app


app = init_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run("app.main:app")
