from fastapi import FastAPI

from app.router.socket_server.socket_server_router import socket_server_router

app = FastAPI()


# uvicorn app.main:app --reloa
@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(socket_server_router)