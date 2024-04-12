import socket

def send_command_to_program1(command):
    '''
    Данная функция принимает команду для отправки на сервер
    слова-слова
    '''
    host = '127.0.0.1'
    port = 12345 #диапазон от 1024 до 65000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port)) #устанавливает соединение с указанным портом и хостом
        client_socket.sendall(command.encode()) #передача через сокет в байтах
        data = client_socket.recv(1024) #получает данные через сокет до 1024 байт
        with open('updated_programs.json', 'wb') as file: #wb - запись бинарных данных
            file.write(data)
        print(f'Получение обновленных данных от Программы 1')
    #client_socket.close()


# Пример отправки команды "update" для обновления данных
send_command_to_program1('update')
