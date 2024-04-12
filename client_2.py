# -*- coding: utf-8 -*-
import socket
import tkinter as tk

def display_file(data):
    root = tk.Tk()
    text = tk.Text(root)
    text.insert(tk.END, data.decode('utf-8'))
    text.pack()
    root.mainloop()

def main():
    HOST = (socket.gethostname(), 4444)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(HOST)
    server_socket.send('2'.encode('utf-8'))
    print("Подключено к серверу")

    user_input = input("Введите команду ('numbers' для отправки чисел, 'file' для запроса файла): ")

    numbers = ' '
    if user_input == 'numbers':
        while True:
            numbers_input = input("Введите числа:")
            numbers += numbers_input + ' '

            if numbers_input == ' ':
                break
        server_socket.send(numbers.encode('utf-8'))

    elif user_input == 'file':
        run_number = input("Введите время запуска программы: ")
        tree_number = input("Введите номер дерева: ")
        request_data = f"file_request {run_number} {tree_number}"
        server_socket.send(request_data.encode('utf-8'))
    else:
        print("Некорректная команда. Попробуйте снова.")

    received_data = b''
    while True:
            data = server_socket.recv(1024)
            if not data:
                break
            received_data += data

    print('Получено от сервера:', received_data.decode('utf-8'))
    display_file(received_data)

if __name__ == "__main__":
    main()