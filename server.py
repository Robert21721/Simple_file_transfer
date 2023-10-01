import socket
import os

def recv_all(client_socket, end_str):
    resp = b''
    end_bytes = end_str.encode()

    while True:
        data = client_socket.recv(50000)

        if not data:
            print('connection closed')
            break

        if data.endswith(end_bytes):
            data = data[:-len(end_bytes)]
            resp += data
            break

        resp += data

    return resp

def check_file_name(file_name):
    if os.path.isfile(file_name):
        name = file_name.split(".")
        new_name = file_name[:-(len(name[-1]) + 1)] + "_copy." + name[-1]
        return check_file_name(new_name)
    else:
        return file_name


HOST = "0.0.0.0"
PORT = 9000

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is listening...")

while True:
    
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    file_name = recv_all(client_socket, "\n\nEND_NAME\n\n").decode()
    client_socket.sendall("OK".encode())
    client_socket.sendall("\n\nEND\n\n".encode())

    pdf_data = b''
    end_bytes = '\n\nEND_FILE\n\n'.encode()

    print(file_name)
    new_name = check_file_name(file_name)

    with open(new_name, 'wb') as received_file:
        while True:
            pdf_data = client_socket.recv(10000)

            if not pdf_data:
                print('connection closed')
                break

            if pdf_data.endswith(end_bytes):
                pdf_data = pdf_data[:-len(end_bytes)]
                received_file.write(pdf_data)
                break

            received_file.write(pdf_data)

    client_socket.sendall("OK".encode())
    client_socket.sendall("\n\nEND\n\n".encode())

    # Close the sockets
    client_socket.close()