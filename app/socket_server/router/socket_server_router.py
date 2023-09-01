import asyncio

from fastapi import APIRouter, HTTPException, Request

from app.socket_server.exception.request_duplication_exception import check_duplicate_request
from app.system_queue.queue import fastapi_queue, socket_server_queue

socket_server_router = APIRouter()

@socket_server_router.get("/start-socket-server")
def start_socket_server():
    print("start socket server")

    fastapi_queue.put(1)

    return True


@socket_server_router.get("/finish-socket-server")
def finish_socket_server():
    print("finish socket server")

    fastapi_queue.put(4)

    return True


@socket_server_router.post("/ai-request-command")
async def ai_request_command(request: Request):
    print("ai-request-command")

    try:
        data = await request.json()
        command = data.get("command")
        data_str = data.get("data")
        print("command: ", command, ", data: ", data_str)

        socket_server_queue.put((command, data_str))
        return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

