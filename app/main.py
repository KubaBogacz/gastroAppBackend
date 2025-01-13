from fastapi import FastAPI
from app.database import Base, engine
from app.routers import drug, user, auth

Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    app = FastAPI(
        title="GastroAppBackend",
        version="0.1.0"
    )

    return app

app = create_app()

# Rejestracja i logowanie
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Obsługa użytkowników
app.include_router(user.router, prefix="/users", tags=["users"])

# Leki
app.include_router(drug.router, prefix="/drugs", tags=["drugs"])
