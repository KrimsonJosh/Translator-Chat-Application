
import socket #for network communication
import threading #for running multiple tasks (multiple clients) at once


HOST = '127.0.0.1' 
PORT = 5000         #

#List to keep track of clients
clients = []

#broadcast broadcasts message message to all clients in the client list
def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

#receives message, and broadcasts it from client client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
        except:
            client.close()
            clients.remove(client)
            break

#receive connections to connect client to the server
def receive_connections():
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
receive_connections()
