import pika

class MessageBroker:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='chat', exchange_type='topic')

    def publish(self, room_name, message):
        self.channel.basic_publish(exchange='chat', routing_key=room_name, body=message)

    def subscribe(self, room_name, callback):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='chat', queue=queue_name, routing_key=room_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def start_consuming(self):
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
