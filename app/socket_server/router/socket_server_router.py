import asyncio

from fastapi import APIRouter, HTTPException, Request

import os
import importlib

script_directory = os.path.dirname(__file__)
print("exception script_directory: ", script_directory)

module_path = "../exception"
absolute_module_path = os.path.abspath(os.path.join(script_directory, module_path))
relative_module_path = os.path.relpath(absolute_module_path, os.path.abspath(os.getcwd()))
relative_exception_module_path_for_importlib = relative_module_path.replace(os.path.sep, ".").lstrip(".")
relative_exception_module_path_for_importlib += ".request_duplication_exception"
print("relative_exception_module_path_for_importlib: ", relative_exception_module_path_for_importlib)

exception_module = importlib.import_module(relative_exception_module_path_for_importlib)
#from app.socket_server.exception.request_duplication_exception import check_duplicate_request

module_path = "../../system_queue"
absolute_module_path = os.path.abspath(os.path.join(script_directory, module_path))
relative_module_path = os.path.relpath(absolute_module_path, os.path.abspath(os.getcwd()))
relative_system_queue_module_path_for_importlib = relative_module_path.replace(os.path.sep, ".").lstrip(".")
relative_system_queue_module_path_for_importlib += ".queue"
print("relative_system_queue_module_path_for_importlib: ", relative_system_queue_module_path_for_importlib)

system_queue_module = importlib.import_module(relative_system_queue_module_path_for_importlib)
#from app.system_queue.queue import fastapi_queue, socket_server_queue

socket_server_router = APIRouter()

@socket_server_router.get("/start-socket-server")
def start_socket_server():
    print("start socket server")

    system_queue_module.fastapi_queue.put(1)

    return True


@socket_server_router.get("/finish-socket-server")
def finish_socket_server():
    print("finish socket server")

    system_queue_module.fastapi_queue.put(4)

    return True


@socket_server_router.post("/ai-request-command")
async def ai_request_command(request: Request):
    print("ai-request-command")

    command = None
    data_str = None

    try:
        data = await request.json()

        if isinstance(data, list):
            for item in data:
                command = item.get("command")
                data_str = item.get("data")
        else:
            command = data.get("command")
            data_str = data.get("data")

        print("command: ", command, ", data: ", data_str)
        system_queue_module.socket_server_queue.put((command, data_str))

        return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@socket_server_router.get("/ai-response")
def ai_response_result():
    print("ai-response-result");

    ai_response_result = system_queue_module.socket_server_response_queue.get()

    return ai_response_result

