import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QPushButton, QLabel, QInputDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import socket
import threading

class MessageReceiver(QThread):
    message_received = pyqtSignal(str)
    
    def __init__(self, client_socket, name):
        super().__init__()
        self.client_socket = client_socket
        self.name = name
        self.running = True

    def run(self):
        while self.running:
            try:
                message = self.receive_message()
                if not message:
                    break
                self.message_received.emit(message)
            except:
                break
    
    def receive_message(self):
        header = self.client_socket.recv(4)
        if not header:
            return None
        msg_length = int.from_bytes(header, 'big')
        message = self.client_socket.recv(msg_length).decode("utf-8")
        return message

    def stop(self):
        self.running = False

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.client_socket = None
        self.init_ui()
        self.connect_to_server()

    def init_ui(self):
        self.setWindowTitle('PyChat')
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Input area
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.returnPressed.connect(self.send_message)
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

    def connect_to_server(self):
        self.name, ok = QInputDialog.getText(self, 'Name Input', 'Enter your name:')
        if not ok or not self.name:
            sys.exit()

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 8888))
            
            # Start message receiver thread
            self.receiver = MessageReceiver(self.client_socket, self.name)
            self.receiver.message_received.connect(self.display_message)
            self.receiver.start()
            
            self.chat_display.append(f"Connected to server as {self.name}")
        except Exception as e:
            self.chat_display.append(f"Failed to connect: {str(e)}")
            self.client_socket = None

    def send_message(self):
        if not self.client_socket:
            return
            
        message = self.message_input.text().strip()
        if message:
            try:
                full_message = f"{self.name} : {message}"
                msg_length = len(full_message).to_bytes(4, 'big')
                self.client_socket.sendall(msg_length + full_message.encode("utf-8"))
                self.message_input.clear()
            except:
                self.chat_display.append("Failed to send message")

    def display_message(self, message):
        self.chat_display.append(message)

    def closeEvent(self, event):
        if self.client_socket:
            self.receiver.stop()
            self.client_socket.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())