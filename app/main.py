import os
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

import os
import importlib

script_directory = os.path.dirname(__file__)
print("main script_directory: ", script_directory)


# uvicorn app.main:app --host 0.0.0.0 --port 8000
if __name__ == '__main__':
    main_process_id = os.getpid()
    print(f"현재 프로세스의 ID: {main_process_id}")

    # 세개 요소 가지고 run_socket_server 함수 실행
    socket_server_process = Process(target=run_socket_server,
                                    args=(fastapi_queue, socket_server_queue, main_process_id, ))

    # socket_server_process 함수 실행
    socket_server_process.start()

    print("socket_server_process: ", socket_server_process)

    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

