from fastapi import FastAPI
from taskmanager.database import create_db_and_tables
from taskmanager.api import router


app = FastAPI()
app.include_router(router)
create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)