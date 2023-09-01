import importlib
from asyncio import sleep

socket_server_module = importlib.import_module("app.includes.Mercenary-Socket-Server.socket_server")
server_instance = None


def run_socket_server(fastapi_queue, socket_server_queue):
    print("run_socket_server")
    server_instance = socket_server_module.SocketServer('0.0.0.0', 33333)

    # 큐를 통해 FastAPI 애플리케이션과 통신
    while True:
        command = fastapi_queue.get()
        print("receive - command: ", command)

        if command == 4:
            server_instance.kill_all_process()
            break
        elif command == 1:
            server_instance.start()
        elif command == 333:
            data_str = fastapi_queue.get()
            transmitter = server_instance.get_transmitter()
            transmitter.put_command_data(command, data_str)

        sleep(0.5)