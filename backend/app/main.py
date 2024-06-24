from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import image_handler, tag_handler, image_tag_handler
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:8080",  # Frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Image Database API"}

app.include_router(image_handler.router)
app.include_router(tag_handler.router)
app.include_router(image_tag_handler.router)

# Mount the static directory to serve static files
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Get the base directory
static_dir_path = os.path.join(base_dir, 'frontend\\static')  # Construct the static directory path
print(static_dir_path)
app.mount("/frontend/static", StaticFiles(directory=static_dir_path), name="static")