import pika
import json
import threading
from typing import Callable


class ConsumidorMensagens:
    EXCHANGE_GROUP = 'clientes1-3'

    def __init__(self, callback: Callable[[str, str], None]):
        self.callback = callback
        self.factory = pika.ConnectionParameters(
            host='189.8.205.54',
            virtual_host='thanos',
            credentials=pika.PlainCredentials('senai', 'senai@'),
        )
        self.connection = pika.BlockingConnection(self.factory)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.EXCHANGE_GROUP,
            exchange_type='fanout',
            durable=True,
        )
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.EXCHANGE_GROUP, queue=self.queue_name)

    def start_consuming(self):
        def callback(ch, method, properties, body):
            data = json.loads(body.decode('UTF-8'))
            msg = data.get('message')
            sender_name = data.get('sender_name')
            print(f" [!] Mensagem recebida de {sender_name}: '{msg}'")
            self.callback(msg, sender_name)

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=True,
        )
        print(' [*] Aguardando mensagens. Para sair, pressione CTRL+C')
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()
        self.connection.close()


if __name__ == '__main__':
    def print_message(msg, sender):
        print(f"Received message from {sender}: {msg}")

    consumidor = ConsumidorMensagens(print_message)
    consumidor_thread = threading.Thread(target=consumidor.start_consuming)
    consumidor_thread.start()
