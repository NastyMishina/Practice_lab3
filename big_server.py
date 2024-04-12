# -*- coding: utf-8 -*-
import socket
#!/usr/bin/python3

import socket
import asyncio
import os
import json
import datetime
import struct


def read_from_json():
    if os.path.exists("programs.json"):
        with open("programs.json", "r") as file:
            data_file = json.load(file)
        return data_file['programs']
    else:
        return ['dir', 'echo hello!']
    
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


class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.server = None

    def start(self, is_async=True):
        if is_async:
            asyncio.run(self._async_start())
        

    async def handle_client(self, reader, writer):
        res = None
        input_data = await reader.read(1)
        input_data = input_data.decode('utf-8')
        if input_data == "2":
            print("sofia")
            res = await self.sofia(reader)
        elif input_data == "1":
            print("nastya")
            res = await self.nastya(reader, writer)
        if res:
            writer.write(res.encode('utf-8'))
            writer.close()
            await writer.wait_closed()

    async def nastya(self, reader, writer):

        programs = read_from_json()
        dir_files = dict([(f"./{prog}_dir" , []) for prog in programs])

        get_answ = await reader.read(1024)
        action = struct.unpack('i', get_answ)[0]

        if action == 1:
            data = await reader.read(1024)
            name_size = struct.unpack(f'I', data[:struct.calcsize('I')])[0]
            data_decoded = struct.unpack(f'I{name_size}s', data)[1].decode()
            programs.append(data_decoded)
            dir_files[f'./{data_decoded}_dir'] = []

            create_folders_and_files([data_decoded])
            files = run_programs(programs, dir_files)
            write_to_json(files, programs) 

        elif action == 2:
            buffer_size = 4096
            name = await reader.read(buffer_size)
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
            writer.write(bytes_read)
        


    async def _async_start(self):
            self.server = await asyncio.start_server(
                self.handle_client, self._host, self._port)
            addr = self.server.sockets[0].getsockname()
            print(f'Сервер запущен на {addr}')
            async with self.server:
                await self.server.serve_forever()

if __name__ == "__main__":
        HOST = socket.gethostname()
        PORT = 4444
        server = Server(HOST, PORT)
        server.start()