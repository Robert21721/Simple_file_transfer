import socket
import sys
import os
from pathlib import Path

def send_file(path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('82.210.153.205', 9000))

    file_name = os.path.basename(path)

    client_socket.sendall(file_name.encode())
    client_socket.sendall("\n\nEND_NAME\n\n".encode())

    resp = recv_all(client_socket).decode()
    if resp != "OK":
        print("Communication Failed")
        exit(-1)

    # Open and read the PDF file
    with open(path, 'rb') as pdf_file:
        pdf_data = pdf_file.read()

    # Send the PDF data to the client
    client_socket.sendall(pdf_data)
    client_socket.sendall("\n\nEND_FILE\n\n".encode())

    resp = recv_all(client_socket).decode()
    if resp != "OK":
        print("Communication Failed")
        exit(-1)

    client_socket.close()


def recv_all(client_socket):
    resp = b''
    end_bytes = '\n\nEND\n\n'.encode()

    while True:
        data = client_socket.recv(1024)

        if not data:
            print('connection closed')
            break

        if data.endswith(end_bytes):
            data = data[:-len(end_bytes)]
            resp += data
            break

        resp += data

    return resp


if __name__ == "__main__":

    num_arguments = len(sys.argv) - 1

    if num_arguments != 2:
        print("Incorrect Command - You have these options:\n")
        print("python3 send.py -f [file_path]")
        print("python3 send.py -d [dir_path ]")
        exit(-1)


    if sys.argv[1] == "-f":
        path_file = sys.argv[2]
        send_file(path_file)

    elif sys.argv[1] == "-d":
        path_dir = sys.argv[2]

        directory_path = Path(path_dir)

        # Iterate through each file in the directory
        for file in directory_path.iterdir():
            # Check if the item is a file (not a subdirectory)
            if file.is_file():
                # Process the file
                path_file = file.absolute()
                send_file(path_file)

    else:
        print("Incorrect Command - You have these options:\n")
        print("python3 send.py -f [file_path]")
        print("python3 send.py -d [dir_path ]")
        exit(-1)