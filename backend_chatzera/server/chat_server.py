import threading
from message_broker import MessageBroker

class ChatServer:
    def __init__(self):
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

    def start(self):
        # Aqui você pode iniciar o loop principal para aceitar conexões
        pass

if __name__ == "__main__":
    server = ChatServer()
    server.start()
