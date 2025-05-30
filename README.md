# PyChat Room

A simple chat room application built with Python, featuring both command-line and GUI interfaces. The application uses socket programming for network communication and PyQt5 for the graphical user interface.

## Features

- Real-time chat messaging
- Multiple client support
- Both GUI and command-line interfaces
- Simple and intuitive user interface
- Message broadcasting to all connected clients

## Prerequisites

Before running the application, make sure you have Python 3.x installed and the following dependencies:

```bash
pip install PyQt5
```

## Project Structure

```
pyChatRoom/
├── server.py        # Chat server implementation
├── client.py        # Command-line client
├── client_gui.py    # GUI client implementation
└── README.md        # This file
```

## Usage

### Starting the Server

1. Open a terminal in the project directory
2. Run the server:
```bash
python server.py
```
The server will start listening on localhost:8888

### Running the GUI Client

1. Open a new terminal
2. Launch the GUI client:
```bash
python client_gui.py
```
3. Enter your name when prompted
4. Start chatting!

### Running the Command-line Client

1. Open a new terminal
2. Launch the command-line client:
```bash
python client.py
```
3. Enter your name when prompted
4. Type messages and press Enter to send
5. Type 'q' to quit

## Features Explanation

### Server (server.py)
- Handles multiple client connections using threading
- Broadcasts messages to all connected clients
- Manages client disconnections gracefully

### GUI Client (client_gui.py)
- Modern PyQt5-based interface
- Real-time message updates
- Clean disconnection handling
- Message input with both Enter key and Send button support
- Scrollable chat history

### Command-line Client (client.py)
- Simple text-based interface
- Lightweight implementation
- Suitable for basic testing and development

## Implementation Details

The application uses:
- Socket programming for network communication
- Threading for handling multiple clients
- Message length headers for reliable message transmission
- PyQt5 for the graphical user interface
- QThread for non-blocking message reception in GUI

## Common Issues and Solutions

1. **Port Already in Use**
   - Ensure no other instance of the server is running
   - Change the port number in both server and client files

2. **Connection Refused**
   - Make sure the server is running before starting clients
   - Verify the host and port settings

## Contributing

Feel free to fork this project and submit pull requests. You can also open issues for bugs or feature requests.

## License

This project is open source and available under the MIT License.
