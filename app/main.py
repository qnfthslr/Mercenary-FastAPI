from multiprocessing import Process
from fastapi import FastAPI

from app.includes.project_importer import import_all
import_all()

from app.socket_server.generator import run_socket_server
from app.system_queue.queue import fastapi_queue, socket_server_queue
from app.socket_server.router.socket_server_router import socket_server_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(socket_server_router)


# uvicorn app.main:app --host 0.0.0.0 --port 8000
if __name__ == '__main__':
    socket_server_process = Process(target=run_socket_server, args=(fastapi_queue, socket_server_queue, ))
    socket_server_process.start()
    print("socket_server_process: ", socket_server_process)

    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

