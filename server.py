import os
import time
import datetime
import json
import socket
import struct

# Функция для создания папок при первом запуске программы
def create_folders_and_files(programs):
    for program in programs:
        folder_path = f"./{program}_dir"
        os.makedirs(folder_path, exist_ok=True)

# Функция для запуска программ и записи вывода в файлы
def run_programs(programs, dict_file, new_prog=None):
    for program in programs:
        folder_path = f"./{program}_dir" 
        file_name = f"{folder_path}/output{datetime.datetime.now().strftime('%H.%M.%S')}.txt"   # Запись времени "создания" файла 
        with open(file_name, "a+") as file:                                                           # происходит через точку
            file.write(f"Output for {program}:\n")                                                             
            output = os.popen(program).read()
            file.write(output)
        dict_file[folder_path].append(file_name)
    return dict_file

# Функция для записи программ и их папок в файл объектно-ориентированного формата данных (json)
def write_to_json(data, prog):
    with open("programs.json", "w+") as file:
        data['programs'] = prog
        json.dump(data, file)

# Функция для чтения программ из файла объектно-ориентированного формата данных (json)
def read_from_json():
    if os.path.exists("programs.json"):
        with open("programs.json", "r") as file:
            data_file = json.load(file)
        return data_file['programs']
    else:
        return ['dir', 'echo hello!']

# Функция для установления сетевого взаимодействия с другой программой
def establish_connection():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12346))
    server_socket.listen(1)
    print("Сервер запущен и ожидает подключения...")

    conn, addr = server_socket.accept()
    get_answ = conn.recv(1024)
    action = struct.unpack('i', get_answ)[0]
    print(f"Подключение установлено с {addr}")

    with conn:
        if action == 1:
            data = conn.recv(1024)
            name_size = struct.unpack(f'I', data[:struct.calcsize('I')])[0]
            data_decoded = struct.unpack(f'I{name_size}s', data)[1].decode()
            programs.append(data_decoded)
            dir_files[f'./{data_decoded}_dir'] = []

            create_folders_and_files([data_decoded])
            files = run_programs(programs, dir_files)
            write_to_json(files, programs) 

        elif action == 2:
            buffer_size = 4096
            name = conn.recv(buffer_size)
            program_name_size = struct.unpack(f'I', name[:struct.calcsize('I')])[0]
            program_name = struct.unpack(f'I{program_name_size}s', name)[1].decode()
            file_name = [prog for prog in read_from_json() if prog == program_name]
            folder_name = f"./{file_name[0]}_dir"
            send_string = ''

            if os.path.exists("programs.json"):
                with open("programs.json", "r") as file:
                    data_file = json.load(file)[folder_name]

            for file_read in data_file: 
                with open(file_read, 'r') as file:
                    string_read = file.read(buffer_size)
                send_string += string_read

            bytes_read = struct.pack(f'I{len(send_string)}s', len(send_string), send_string.encode())
            conn.send(bytes_read)
            conn.close()
        
# Основная часть программы
if __name__ == '__main__':
    programs = read_from_json()
    dir_files = dict([(f"./{prog}_dir" , []) for prog in programs])
    establish_connection()


        
