from fastapi import FastAPI
from routes.routes import router as auth_router
from routes.note_routes import router as notes_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(notes_router)