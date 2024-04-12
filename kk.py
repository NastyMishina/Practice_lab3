import os
import json
import socket

def get_programs_in_path(path):
    programs = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            programs.append(os.path.join(dirpath, filename))
    return programs

def get_system_path_programs():
    system_path = os.getenv('PATH')
    system_path_list = system_path.split(os.pathsep)
    programs = []
    for path in system_path_list:
        programs.extend(get_programs_in_path(path))
    return programs


def create_programs_json_file(filename):
    '''
    Данная функция создает JSON файл
    '''

    programs = get_system_path_programs()

    data = {}
    for program in programs:
        folder, program_name = os.path.split(program)
        folder_data = data
        for subfolder in folder.split(os.sep):
            folder_data = folder_data.setdefault(subfolder, {})
        folder_data[program_name] = None

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def start_server():
    '''
    Данная функция выполняет:
    Прием json файла, установку соединения,
    передачу данных между клиентом и сервером
    '''
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if data == b'update':
                    create_programs_json_file('programs.json')
                    with open('programs.json', 'rb') as file:
                        conn.sendall(file.read())

start_server()
