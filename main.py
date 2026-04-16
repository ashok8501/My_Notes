from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routes.notes import router as notes_router
from routes.auth import router as auth_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Routes
app.include_router(notes_router, prefix="/notes", tags=["Notes"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


# Home Page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})