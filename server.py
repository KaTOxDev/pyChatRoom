import socket
import threading

print("Chat Server By KaTO  ...")

clients = []
def send_message(message , targets):
    for cc in targets:
        # Convert the length of the message to a 4-byte header
        msg_length = len(message).to_bytes(4, 'big')

        # Send the header followed by the message
        cc.sendall(msg_length + message.encode("utf-8"))
    
def receive_message(client_socket):
    # Receive the header (message length)
    header = client_socket.recv(4)
    if not header:
        return None

    # Convert the header to an integer
    msg_length = int.from_bytes(header, 'big')

    # Receive the message based on the length
    message = client_socket.recv(msg_length).decode("utf-8")
    return message

def handle_client(client_socket, address):
    while True:
        try:
            message = receive_message(client_socket)
            if not message:
                break
            print(f"Received message from client {address[0]}:{address[1]}: {message}")
            send_message(message , clients)
        except ConnectionResetError:
            break
    print(f"Client {address[0]}:{address[1]} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        print(f"Connected to client: {address[0]}:{address[1]}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == '__main__':
    host = 'localhost'
    port = 8888
    start_server(host, port)
