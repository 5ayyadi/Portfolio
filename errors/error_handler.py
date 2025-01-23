from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def add_default_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "msg": f"Oops! Error ({str(exc)}) Happened",
                "status_code": 500,
                "result": None
            },
        )

    return app
