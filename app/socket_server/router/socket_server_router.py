import asyncio

from fastapi import APIRouter, HTTPException, Request

import os
import importlib

# 현재 스크립트 파일이 위치한 디렉토리 경로 저장
script_directory = os.path.dirname(__file__)
print("exception script_directory: ", script_directory)

# exception 모듈 경로 설정
module_path = "../exception"
absolute_module_path = os.path.abspath(os.path.join(script_directory, module_path))
relative_module_path = os.path.relpath(absolute_module_path, os.path.abspath(os.getcwd()))
relative_exception_module_path_for_importlib = relative_module_path.replace(os.path.sep, ".").lstrip(".")
relative_exception_module_path_for_importlib += ".request_duplication_exception"
print("relative_exception_module_path_for_importlib: ", relative_exception_module_path_for_importlib)

exception_module = importlib.import_module(relative_exception_module_path_for_importlib)
# from app.socket_server.exception.request_duplication_exception import check_duplicate_request

# system_queue 모듈 경로 설정
module_path = "../../system_queue"
absolute_module_path = os.path.abspath(os.path.join(script_directory, module_path))
relative_module_path = os.path.relpath(absolute_module_path, os.path.abspath(os.getcwd()))
relative_system_queue_module_path_for_importlib = relative_module_path.replace(os.path.sep, ".").lstrip(".")
relative_system_queue_module_path_for_importlib += ".queue"
print("relative_system_queue_module_path_for_importlib: ", relative_system_queue_module_path_for_importlib)

# 동적으로 불러온 모듈 저장
system_queue_module = importlib.import_module(relative_system_queue_module_path_for_importlib)
#from app.system_queue.queue import fastapi_queue, socket_server_queue

socket_server_router = APIRouter()

@socket_server_router.get("/start-socket-server")
def start_socket_server():
    print("start socket server")

    system_queue_module.fastapi_queue.put(1)
    # 1을 추가하여 시작 명령 전달

    return True


@socket_server_router.get("/finish-socket-server")
def finish_socket_server():
    print("finish socket server")

    system_queue_module.fastapi_queue.put(4)
    # 4를 추가하여 소켓 서버 종료 명령 전달

    return True


# ---- 이쪽에다가 Vue에서 받을 router 만들어주면 된다. ㅇㅇㅇㅇㅇㅇㅇ
@socket_server_router.post("/ai-request-command")
async def ai_request_command(request: Request):
    # 요청을 받으면
    print("ai-request-command")

    command = None
    data_str = None

    try:
        # fastapi에서 json으로 받은 요청을 비동기적으로 읽어와서  list로 변환
        data = await request.json()

        if isinstance(data, list): # data가 list면
            for item in data:
                # command에 해당하는 값 추출하여 command 변수에 할당
                command = item.get("command")
                # data에 해당하는 값 추출하여 data_str 변수에 할당
                data_str = item.get("data")
        else: # list가 아닐 경우 (dictionary 일 것임)
            command = data.get("command") # 이하 동문
            data_str = data.get("data")

        print("command: ", command, ", data: ", data_str)
        system_queue_module.socket_server_queue.put((command, data_str))
        # 추출한 명령과 데이터를 system_queue_module 통신하는 Queue에 넣음

        return True

    # 예외 일때
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # 에러 코드 500 설정과 동시에 오류에 대한 설명


@socket_server_router.get("/ai-response")
def ai_response_result():
    print("ai-response-result");

    ai_response_result = system_queue_module.socket_server_response_queue.get()

    return ai_response_result

