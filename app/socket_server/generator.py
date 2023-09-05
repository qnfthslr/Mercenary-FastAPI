import importlib
import multiprocessing
import queue
import signal
from multiprocessing import Process
from time import sleep

socket_server_module = importlib.import_module("app.includes.Mercenary-Socket-Server.socket_server")
server_instance = None

import os


# 사실 이 파트는 command_controller 라고 만드는 것이 더 좋았을 것이다
def run_socket_server(fastapi_queue, socket_server_queue, main_process_id):
    print("run_socket_server")
    #server_instance = socket_server_module.SocketServer('0.0.0.0', 33333)
    server_instance = None
    main_socket_process = None

    receiver_pid = None
    transmitter_pid = None

    transmitter = None

    current_pid = os.getpid()
    print("run_socket_server(command_controller) pid: ", current_pid)

    pid_queue = multiprocessing.Queue()

    # 큐를 통해 FastAPI 애플리케이션과 통신
    while True:
        try:
            command = fastapi_queue.get(block=False)
            print("receive - command: ", command)

            if command == 4:
                if main_socket_process and main_socket_process.is_alive():
                    socket_pid = main_socket_process.pid
                    print("socket pid: ", socket_pid)

                    server_instance = None

                    try:
                        os.kill(receiver_pid, signal.SIGTERM)
                        print(f"SIGINT signal sent to receiver process {receiver_pid}.")

                        os.kill(transmitter_pid, signal.SIGTERM)
                        print(f"SIGINT signal sent to transmitter process {transmitter_pid}.")

                        os.kill(socket_pid, signal.SIGTERM)
                        print(f"SIGINT signal sent to socket process {socket_pid}.")

                        #main_socket_process.terminate()

                    except ProcessLookupError:
                        print(f"PID {socket_pid} does not correspond to a running process.")
                    except OSError as e:
                        print(f"An error occurred while sending the signal: {e}")

                    #main_socket_process.join()  # Wait for the process to complete (optional)
                    #main_socket_process.terminate()
                    main_socket_process = None
                    transmitter = None

                    print("All Clear")

                    print("Finish to clean socket")
                else:
                    print("Socket server process is not running.")

            elif command == 1:
                if main_socket_process and main_socket_process.is_alive():
                    # Stop the existing process gracefully
                    main_socket_process.terminate()
                    #main_socket_process.join()
                    main_socket_process = None
                    print("Stopped the existing Socket server process.")

                server_instance = socket_server_module.SocketServer('0.0.0.0', 33333)
                main_socket_process = Process(target=server_instance.start,
                                              args=(fastapi_queue, socket_server_queue, pid_queue, ))
                main_socket_process.start()

                sleep(5)

                pid_data = pid_queue.get()
                print("pid_data: ", pid_data)

                if pid_data[0] == 'rx':
                    receiver_pid = pid_data[1]
                else:
                    transmitter_pid = pid_data[1]

                pid_data = pid_queue.get()
                print("pid_data: ", pid_data)

                if pid_data[0] == 'rx':
                    receiver_pid = pid_data[1]
                else:
                    transmitter_pid = pid_data[1]

                print("tx pid: ", transmitter_pid)
                print("rx pid: ", receiver_pid)

                # server_instance = socket_server_module.SocketServer('0.0.0.0', 33333)
                # main_socket_process = Process(target=server_instance.start, args=(fastapi_queue, socket_server_queue,))
                # main_socket_process.start()

            elif command == 333:
                print("AI Command")
                data_str = fastapi_queue.get()
                transmitter = server_instance.get_transmitter()
                transmitter.put_command_data(command, data_str)

        except queue.Empty:
            # 큐가 비어 있는 경우 예외 처리
            #print("큐가 비어 있습니다.")
            sleep(0.5)

