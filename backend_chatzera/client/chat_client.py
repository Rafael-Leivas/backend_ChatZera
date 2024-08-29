import pika
import threading

class ChatClient:
    def __init__(self, client_id, room_name):
        self.client_id = client_id
        self.room_name = room_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=client_id)
        self.channel.queue_bind(exchange='chat', queue=client_id, routing_key=room_name)

        self.channel.basic_consume(queue=client_id, on_message_callback=self.receive_message, auto_ack=True)

    def send_message(self, message):
        self.channel.basic_publish(exchange='chat', routing_key=self.room_name, body=f"{self.client_id}: {message}")

    def receive_message(self, ch, method, properties, body):
        print(f"Received: {body.decode()}")

    def start(self):
        threading.Thread(target=self.channel.start_consuming).start()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    client = ChatClient('user1', 'general')
    client.start()
    while True:
        msg = input("Enter message: ")
        client.send_message(msg)