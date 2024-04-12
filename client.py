import socket
import struct

HOST = (socket.gethostname(), 4444)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(HOST)
print("Client conected to", HOST)
client_socket.send('1'.encode('utf-8'))

print("1. Добавить новую программу")
print("2. Получить файл с выводом программы")

choice = int(input("Выберите действие (1/2): "))
packed_choice = struct.pack('i', choice)
client_socket.send(packed_choice)

while True:
    if choice == 1:
        new_program_name = input("Введите имя новой программы: ")
        pack_prog = struct.pack(f'I{len(new_program_name)}s', len(new_program_name), new_program_name.encode())
        client_socket.send(pack_prog)

    elif choice == 2:
        program_name = input("Введите имя программы для получения файла с выводом: ")
        packed_name = struct.pack(f'I{len(program_name)}s', len(program_name), program_name.encode())
        client_socket.send(packed_name)

        expected_size = 4096
        data = client_socket.recv(4096)
        received_size = struct.unpack(f'I', data[:struct.calcsize('I')])[0]
        bytes_string = struct.unpack(f'I{received_size}s', data)[1]

        while received_size > 0:
            current_size = received_size if received_size < expected_size else expected_size

            data_size = struct.unpack(f'I', data[:struct.calcsize('I')])[0]
            bytes_string += struct.unpack(f'I{data_size}s', data)[1]
            
            received_size -= current_size

        received_string = bytes_string.decode()
        with open(f'Output_{program_name}.txt', 'w') as file:
            file.write(received_string)
        print(received_string)
    client_socket.close()
