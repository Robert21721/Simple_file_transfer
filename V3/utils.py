HOST = '0.0.0.0'
PORT = 9000

end_name = '\n\t\t\tEND_NAME\t\t\t\n'
end_file = '\n\t\t\tEND_FILE\t\t\t\n'
end_ok   = '\n\t\t\t___OK___\t\t\t\n'

len_end_str = 16 # len(end_name) and len(end_file) and len(end_ok)

command_list =  '''
    - '?'                         - Help

    - 'q' or 'quit'               - Exit

    - 'enter send mode' or 'esm'  - Action needed before sending a file
        <file_path> - After entering in send mode you can give the path to the file

    - 'enter recv mode' or 'erm'  - Action needed before receiving a file
                '''

def recv_all(client_socket):
    global end_name, end_file, end_ok, len_end_str
    resp = b''
    end_name_bin = end_name.encode()
    end_file_bin = end_file.encode()
    end_ok_bin = end_ok.encode()

    while True:
        data = client_socket.recv(1024)

        if not data:
            print('connection closed')
            break

        if data.endswith(end_name_bin) or data.endswith(end_file_bin) or data.endswith(end_ok_bin):
            data = data[:-len_end_str]
            resp += data
            break

        resp += data

    return resp