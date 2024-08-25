import socket
import threading
from utils import *

# List to keep track of connected clients
clients = {}
sem = threading.Semaphore(0)
transmit = False

# Handle each client connection
def handle_client(client_socket, address):
    global sem, transmit, clients

    print(f"[NEW CONNECTION] {address} connected.")
    
    while True:
        try:
            clients[client_socket] = 'start'
            # Receiving messages from the client
            message = recv_all(client_socket)
            if not message:
                break
            
            message = message.decode()
            print(f"[{address}] {message}")

            match message:
                case 'esm':
                    print(f'[{address}] Enter in esm mode')
                    clients[client_socket] = 'esm'
                    client_socket.sendall('OK'.encode())
                    client_socket.sendall(end_ok.encode())
                    # while True:
                        # recv file name
                    file_name = recv_all(client_socket).decode()
                    if not file_name:
                        clients[client_socket] = 'start'
                        break

                    print(f"[{address}] File Name: {file_name}")

                    # response to file name
                    client_socket.sendall("OK".encode())
                    client_socket.sendall(end_ok.encode())

                    print(f"[{address}] Recv data for {file_name}")
                    file_data = recv_all(client_socket)

                    client_socket.sendall("OK".encode())
                    client_socket.sendall(end_ok.encode())
                    print(f"[{address}] Recv ended for {file_name}")

                    for cl_sock in clients.keys():
                        if client_socket != cl_sock and clients[cl_sock] == 'erm':
                            print(f"[{address}] Sending to client {cl_sock}")
                            cl_sock.sendall(file_name.encode())
                            cl_sock.sendall(end_name.encode())

                            sem.acquire()

                            if transmit == True:
                                print(f'Client {cl_sock} accepted')
                                cl_sock.sendall(file_data)
                                cl_sock.sendall(end_file.encode())
                                transmit = False
                case 'erm':
                    print(f'[{address}] Enter in erm mode')
                    clients[client_socket] = 'erm'
                    # while True:

                    message = recv_all(client_socket).decode()
                    if not message:
                        clients[client_socket] = 'start'
                        break

                    if message == 'OK':
                        transmit = True
                    else:
                        transmit = False

                    sem.release()
                    
        except Exception as e:
            print(e)
            break
    
    # Remove the client and close the connection
    print(f"[DISCONNECTED] {address} disconnected.")
    clients.pop(client_socket)
    client_socket.close()

# Main function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening.append( on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        clients[client_socket] = 'start'
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()