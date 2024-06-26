# backend

### Navigate to the project directory
```
cd backend
```
### Create the Virtual Python environment
```
python -m venv env
```
### Start the Virtual Environment
```
source env/bin/activate   # On Windows, use `env\Scripts\activate`
```
### Install dependencies
```
pip install -r requirements.txt
```
### Initialize the database (/backend/test.db)
```
py -c 'from app.storage.db import create_tables; create_tables()'
```
### Run the server
```
uvicorn app.main:app --reload
```