from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Sample Management API", version="1.0.0")
app.include_router(router, prefix="/api")
