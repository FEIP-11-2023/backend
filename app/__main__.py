import fastapi
import uvicorn
from app.auth.router import router as auth_subrouter

app = fastapi.FastAPI()


app.include_router(auth_subrouter, prefix="/api/v1/auth/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
