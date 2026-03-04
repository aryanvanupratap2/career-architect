from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from db.database import engine
from auth.routes import router as auth_router
from career.routes import router as career_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    print("🚀 App started")

    yield

    # Shutdown
    await engine.dispose()
    print("🛑 App shutdown")


app = FastAPI(lifespan=lifespan)

# CORS (needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(career_router)