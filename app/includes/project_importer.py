import os
import sys
import importlib.util


def import_all():
    mercenary_socket_server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Mercenary-Socket-Server')
    sys.path.append(mercenary_socket_server_path)

    print("mercenary_socket_server_path: ", mercenary_socket_server_path)

    # Mercenary-Socket-Server 내의 모든 .py 파일을 로드
    for module_filename in os.listdir(os.path.join(mercenary_socket_server_path)):
        if module_filename.endswith('.py'):
            module_name = module_filename[:-3]
            module_path = os.path.join(mercenary_socket_server_path, module_filename)

            # 모듈 스펙 생성
            module_spec = importlib.util.spec_from_file_location(module_name, module_path)

            # 모듈 로드
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)

