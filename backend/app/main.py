from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import image_handler, tag_handler, image_tag_handler

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Image Database API"}

app.include_router(image_handler.router)
app.include_router(tag_handler.router)
app.include_router(image_tag_handler.router)

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")