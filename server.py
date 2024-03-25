import socket
import threading

# Server configuration: IP address and port
HOST = '127.0.0.1'
PORT = 65432

# Set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Lists to keep track of clients and their nicknames
clients = []
nicknames = []
# Dictionary to store registered usernames and their passwords
credentials = {}

# Broadcasts a message to all clients
def broadcast(message, exclude=None):
    for client in clients:
        if client != exclude:
            client.send(message)

# Sends a private message to a specific client based on their nickname
def send_private_message(nickname, message):
    if nickname in nicknames:
        index = nicknames.index(nickname)
        clients[index].send(message.encode('utf-8'))
        return True
    return False

# Handles a login request from a client
def handle_login(client, username, password):
    if username in credentials and credentials[username] == password:
        clients.append(client)
        nicknames.append(username)
        broadcast(f"{username} joined the chat!".encode('utf-8'), exclude=client)
        client.send("Login successful!".encode('utf-8'))
    else:
        client.send("Login failed. Username or password incorrect.".encode('utf-8'))

# Handles a registration request from a client
def handle_registration(client, username, password):
    if username in credentials:
        client.send("Registration failed. Username already taken.".encode('utf-8'))
    else:
        credentials[username] = password
        client.send("Registration successful. You can now log in.".encode('utf-8'))

# Handles broadcasting a public message from a client
def handle_public_message(client, *args):
    public_message = ' '.join(args)
    broadcast_message = f"{nicknames[clients.index(client)]}: {public_message}".encode('utf-8')
    broadcast(broadcast_message, exclude=client)

# Handles sending a private message from one client to another
def handle_private_message(client, target_nickname, *args):
    priv_message = ' '.join(args)
    if not send_private_message(target_nickname, f"Private message from {nicknames[clients.index(client)]}: {priv_message}"):
        client.send(f"User {target_nickname} not found.".encode('utf-8'))

# Handles a request to list all online users
def handle_list_command(client):
    client.send(f"Online users: {', '.join(nicknames)}".encode('utf-8'))

# Handles a logout request from a client
def handle_logout(client):
    try:
        index = clients.index(client)
        nickname = nicknames.pop(index)
        clients.pop(index)
        broadcast(f"{nickname} has left the chat.".encode('utf-8'))
        client.close()
        print(f"{nickname} logged out.")
    except ValueError:
        print("Client was not in the list.")

# Handles incoming messages from a client and processes commands
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            command, *args = message.split()  # Split the message into command and arguments

            # Determine the command type and call the appropriate handler
            if command == 'LOGIN':
                handle_login(client, *args)
            elif command == 'REGISTER':
                handle_registration(client, *args)
            elif command == 'MSG':
                handle_public_message(client, *args)
            elif command == 'PRIVMSG':
                handle_private_message(client, *args)
            elif command == 'LIST':
                handle_list_command(client)
            elif command == 'LOGOUT':
                handle_logout(client)
                break  # Exit loop to end thread when client logs out
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # Exit loop on error


def receive():
    while True:
        client, address = server.accept()  # Accept new connection
        print(f"Connected with {str(address)}")
        client.send("Welcome! Please register or login to continue.".encode('utf-8'))  # Send welcome message
        thread = threading.Thread(target=handle_client, args=(client,))  # Start new thread for client
        thread.start()

print(f"Server listening on {HOST}:{PORT}")
receive()