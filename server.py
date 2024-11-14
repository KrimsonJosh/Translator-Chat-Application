import socket  #For network communication
import threading  #For running multiple tasks (multiple clients) at once

HOST = ''  
PORT = 5000        

#List to keep track of clients
clients = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
        except:
            client.close()
            if client in clients:
                clients.remove(client)
            break

def receive_connections():
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    receive_connections()
