# Image-DB
## Overview
Image-DB is a project aimed at creating an easily deployable database to efficiently find images stored on your local computer or online through public URLs. With Image-DB, you can tag images with multiple tags and easily look them up based on those tags, making it simpler to manage and retrieve images without remembering file names.

This project was born out of a personal need to manage a vast collection of art reference images. Instead of manually searching through folders, Image-DB allows you to store and search for images by tags, making it a powerful tool for artists, photographers, and anyone who needs to manage large collections of images.

The next step for easy deployment, will be to make it containerized and be able to run with Docker and DockerFiles.

I aspire for the final version to be turned into an executable.

## High-Level Architecture
The frontend uses Vue.js 3 as a one-and-done. Components handle the interactions with the backend and consequently the database.
The backend uses Python’s FastAPI and sqlalchemy.orm to interface with the database.
The database is SQLite for testing feasibility and proof of concept. The finalized form should use PostgreSQL.
##Setup
When this project is finalized, it will be containerized and be able to run with Docker and DockerFiles. For the time being, this is how to get the frontend and backend set up and running.
###Frontend (Requires npm)
1. Navigate to the project directory
```
cd frontend
```
2. Install npm dependencies
```
npm install
```
3. Run the server
```
npm run serve
```
### Backend
1. Navigate to the project directory
```
cd backend
```
2. Create the Virtual Python environment
```
python -m venv env
```
3. Start the Virtual Environment
```
source env/bin/activate   # On Windows, use `env\Scripts\activate`
```
4. Install dependencies
```
pip install -r requirements.txt
```
5. Initialize the database (/backend/test.db)
```
py -c 'from app.storage.db import create_tables; create_tables()'
```
6. Run the server
```
uvicorn app.main:app --reload
```
