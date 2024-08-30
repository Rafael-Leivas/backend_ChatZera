import threading
import socket
from message_broker import MessageBroker

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # O servidor irá escutar até 5 conexões simultâneas
        self.rooms = {}  # Dicionário para gerenciar as salas de chat
        self.clients = {}  # Dicionário para gerenciar os clientes
        self.broker = MessageBroker()

    def create_room(self, room_name):
        if room_name not in self.rooms:
            self.rooms[room_name] = set()

    def add_client(self, client_id, room_name):
        if room_name in self.rooms:
            self.rooms[room_name].add(client_id)
            self.clients[client_id] = room_name

    def remove_client(self, client_id):
        room_name = self.clients.pop(client_id, None)
        if room_name and client_id in self.rooms.get(room_name, set()):
            self.rooms[room_name].remove(client_id)

    def send_message(self, client_id, message):
        room_name = self.clients.get(client_id)
        if room_name:
            self.broker.publish(room_name, message)

    def handle_client(self, client_socket, client_id):
        try:
            room_name = client_socket.recv(1024).decode('utf-8')  # Recebe a sala do cliente
            self.create_room(room_name)
            self.add_client(client_id, room_name)
            self.broker.subscribe(room_name, self.broadcast_message)

            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Message from {client_id}: {message}")
                    self.send_message(client_id, message)
                else:
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.remove_client(client_id)
            client_socket.close()

    def broadcast_message(self, ch, method, properties, body):
        print(f"Broadcasting message: {body.decode()}")

    def start(self):
        print("Server is running...")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_id = addr[1]  # Use o número da porta como ID do cliente (pode-se usar algo mais sofisticado)
            print(f"Client {client_id} connected from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_id))
            client_thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
