import fastapi
import uvicorn
from app.auth.router import router as auth_subrouter
from app.exceptions import ExceptionDescribed
import exceptions
from fastapi.responses import JSONResponse
from fastapi import Request

app = fastapi.FastAPI()


app.include_router(auth_subrouter, prefix="/api/v1/auth")


@app.exception_handler(ExceptionDescribed)
async def exception_described_handler(request: Request, exc: exceptions.ExceptionDescribed):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.code,
            "content": {
                "message": exc.description,  # TODO: implement uuid for every single request to identify.
            }
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
