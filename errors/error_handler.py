from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from errors.error_schema import (
    UnauthorizedAccess,
    NoResultFound,
    WrongInput
)

def add_default_handlers(app: FastAPI):

    @app.exception_handler(UnauthorizedAccess)
    async def wrong_api_key_handler(request: Request, exc: UnauthorizedAccess):
        return JSONResponse(
            status_code= 403,
            content={
                "msg": exc.msg,
                "status_code": 403,
                "result": "The API Key is invalid"
            },
        )
        
    @app.exception_handler(WrongInput)
    async def value_error_handler(request: Request, exc: WrongInput):
        return JSONResponse(
            status_code=400,
            content={
                "msg": (
                    "Value Error occurred, Please Consider this formats: \n "
                    " * Dates: YYYY-MM-DD, \n "
                    " * Email: example@mail.com, \n "
                    " * Phone: +1234567890, \n "
                    " * LinkedIn: https://www.linkedin.com/in/username"
                ),
                "status_code": 400,
                "result": exc.msg
            },
        )

    @app.exception_handler(NoResultFound)
    async def no_result_found_handler(request: Request, exc: NoResultFound):
        return JSONResponse(
            status_code=404,
            content={
                "msg": "No result found for the given query",
                "status_code": 404,
                "result": exc.msg
            },
        )
    
    return app
