from fastapi import FastAPI

from app.includes.project_importer import import_all
import_all()

from app.socket_server.router.socket_server_router import socket_server_router
app = FastAPI()


# uvicorn app.main:app --reloa
@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(socket_server_router)
