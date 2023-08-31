from fastapi import FastAPI

from app.socket_server.router.socket_server_router import socket_server_router

app = FastAPI()


# uvicorn app.main:app --reloa
@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(socket_server_router)