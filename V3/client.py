import socket
import os
from utils import *

def check_file_name(file_name):
    if os.path.isfile(file_name):
        name = file_name.split(".")
        new_name = file_name[:-(len(name[-1]) + 1)] + "_copy." + name[-1]
        return check_file_name(new_name)
    else:
        return file_name

def send_file(path):
    file_name = os.path.basename(path)

    print('Sending file name to server...')
    client_socket.sendall(file_name.encode())
    client_socket.sendall(end_name.encode())

    resp = recv_all(client_socket).decode()
    if resp != "OK":
        print("Communication Failed")
        exit(-1)

    # Open and read the PDF file
    with open(path, 'rb') as pdf_file:
        pdf_data = pdf_file.read()

    print('Sending file data to server...')
    # Send the PDF data to the client
    client_socket.sendall(pdf_data)
    client_socket.sendall(end_file.encode())

    resp = recv_all(client_socket).decode()
    if resp != "OK":
        print("Communication Failed")
        exit(-1)

    print('Done')



def write_to_file(name, data):
        with open(name, 'wb') as received_file:
            received_file.write(data)




if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('95.77.145.18', 9000))

    while True:
        command = input('> ')

        match command:
            case '?':
                print(command_list)

            case 'enter send mode' | 'esm':
                client_socket.sendall('esm'.encode())
                client_socket.sendall(end_ok.encode())

                while True:
                    message = input('Enter file path or q to exit send mode: ')

                    if message == 'quit' or message == 'q':
                        client_socket.sendall('q'.encode())
                        client_socket.sendall(end_ok.encode())
                        break

                    print('---- Send Mode Active ----')
                    
                    send_file(message)
            
            case 'enter recv mode' | 'erm':
                client_socket.sendall('erm'.encode())
                client_socket.sendall(end_ok.encode())

                while True:
                    print('---- Recv Mode Active ----')

                    file_name = recv_all(client_socket).decode()

                    while True:
                        option = input(f'Do you want to receive {file_name}? Type y or n: ')
                        
                        if option == 'n':
                            client_socket.sendall('NOT_OK'.encode())
                            client_socket.sendall(end_ok.encode())
                            break
                        elif option == 'y':
                            client_socket.sendall('OK'.encode())
                            client_socket.sendall(end_ok.encode())

                            file_data = recv_all(client_socket)

                            print("Start saving file...")
                            new_name = check_file_name(file_name)
                            write_to_file(new_name, file_data)

                            print('File saved successfully')
                            break
                    
                    command = input('Type q to exit or enter to continue: ')
                    if command == 'q' or command == 'quit':
                        break
                    
            case 'quit' | 'q':
                break