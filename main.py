from fastapi import FastAPI
from fastapi.responses import FileResponse
from routes.notes import router as notes_router
from routes.auth import router as auth_router

app = FastAPI()

# Routes
app.include_router(notes_router, prefix="/notes", tags=["Notes"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Home Page
@app.get("/")
def home():
    return FileResponse("templates/index.html")