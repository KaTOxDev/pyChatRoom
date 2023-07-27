import socket

import threading
 
def send_message(server_socket, message):
    # Convert the length of the message to a 4-byte header
    msg_length = len(message).to_bytes(4, 'big')

    # Send the header followed by the message
    server_socket.sendall(msg_length + message.encode("utf-8"))
    
def receive_message(server_socket):
    # Receive the header (message length)
    header = server_socket.recv(4)
    if not header:
        return None

    # Convert the header to an integer
    msg_length = int.from_bytes(header, 'big')

    # Receive the message based on the length
    message = server_socket.recv(msg_length).decode("utf-8")
    return message
    
    
def handle_client(client_socket):
    while True:
        try:
            message = receive_message(client_socket)
            if not message:
                break
            if not message.startswith(name):
                print(f"\n{message}")
        except ConnectionResetError:
            break    



    
def start_client(host, port):
    global name
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    name = input("Enter Your Name :")
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    while True:
        message = input("")
        if message == 'q':
            break
        if not message == "":
            send_message(client_socket, name + " : " +message)

    client_socket.close()

if __name__ == '__main__':
    host = 'localhost'
    port = 8888
    start_client(host, port)
