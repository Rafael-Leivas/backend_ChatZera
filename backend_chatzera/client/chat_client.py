import pika
import threading
import time

class ChatClient:
    def __init__(self, client_id, room_name, host='localhost'):
        self.client_id = client_id
        self.room_name = room_name
        self.host = host

    def connect_publisher(self):
        while True:
            try:
                print("Connecting to RabbitMQ for sending messages...")
                self.pub_connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, heartbeat=600, blocked_connection_timeout=300)
                )
                self.pub_channel = self.pub_connection.channel()
                self.pub_channel.exchange_declare(exchange='chat', exchange_type='topic')
                print("Connected to RabbitMQ for sending messages")
                break
            except Exception as e:
                print(f"Failed to connect to RabbitMQ for sending messages: {e}")
                time.sleep(5)

    def connect_consumer(self):
        while True:
            try:
                print("Connecting to RabbitMQ for receiving messages...")
                self.con_connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, heartbeat=600, blocked_connection_timeout=300)
                )
                self.con_channel = self.con_connection.channel()
                self.con_channel.exchange_declare(exchange='chat', exchange_type='topic')
                self.con_channel.queue_declare(queue=self.client_id)
                self.con_channel.queue_bind(exchange='chat', queue=self.client_id, routing_key=self.room_name)
                print("Connected to RabbitMQ for receiving messages")
                break
            except Exception as e:
                print(f"Failed to connect to RabbitMQ for receiving messages: {e}")
                time.sleep(5)

    def send_message(self, message):
        try:
            self.pub_channel.basic_publish(exchange='chat', routing_key=self.room_name, body=f"{self.client_id}: {message}")
            print(f"Sent message: {message}")
        except pika.exceptions.ConnectionClosed as e:
            print(f"Connection closed during sending: {e}. Reconnecting...")
            self.connect_publisher()
            self.send_message(message)
        except Exception as e:
            print(f"Failed to send message: {e}")

    def start_consuming(self):
        def callback(ch, method, properties, body):
            print(f"Received message: {body.decode()}")

        while True:
            try:
                self.con_channel.basic_consume(queue=self.client_id, on_message_callback=callback, auto_ack=True)
                print("Started consuming messages...")
                self.con_channel.start_consuming()
            except pika.exceptions.ConnectionClosed as e:
                print(f"Connection closed during consuming: {e}. Reconnecting...")
                self.connect_consumer()
            except Exception as e:
                print(f"Failed to start consuming: {e}")
                self.connect_consumer()

if __name__ == "__main__":
    client_id = input("Enter your client ID: ")
    room_name = input("Enter the room name: ")
    client = ChatClient(client_id, room_name)

    client.connect_publisher()
    client.connect_consumer()

    consumer_thread = threading.Thread(target=client.start_consuming)
    consumer_thread.start()

    while True:
        msg = input("Enter message: ")
        client.send_message(msg)
