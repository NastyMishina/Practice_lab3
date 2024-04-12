import socket
import os
import time

folder1 = r"C:\Users\ASUS\Documents\testfolder1"  # Папка для синхронизации
folder2 = r"C:\Users\ASUS\Documents\testfolder2"
# Сервер
HOST = '127.0.0.1'  # IP-адрес сервера
PORT = 5000  # Порт сервера


def check_and_send_changes():
    '''
    :return: Отправляет список изменений
    на сервер с использованием
    '''
    source_files = os.listdir(folder1)
    sync_files = os.listdir(folder1)

    changes = []
    for file in source_files:
        if file not in sync_files:
            changes.append(f'add:{file}')
    for file in sync_files:
        if file not in source_files:
            changes.append(f'del:{file}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(str(changes)))
        print('Данные отправлены')


if __name__ == '__main__':
    while True:
        check_and_send_changes()
        time.sleep(5)
