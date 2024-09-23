import pika
import json


class ProdutorMensagens:
    EXCHANGE_GROUP = 'clientes1-3'

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='189.8.205.54',
                virtual_host='thanos',
                credentials=pika.PlainCredentials('senai', 'senai@'),
            )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.EXCHANGE_GROUP,
            exchange_type='fanout',
            durable=True,
        )
        # Lista de observadores (consumidores)
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, msg, sender_name):
        for observer in self.observers:
            observer.update(msg, sender_name)

    def send_message(self, msg, sender_name):
        message_body = json.dumps({
            'message': msg,
            'sender_name': sender_name,
        })
        self.channel.basic_publish(
            exchange=self.EXCHANGE_GROUP,
            routing_key='',
            body=message_body.encode(),
            properties=pika.BasicProperties(
                delivery_mode=2,  # tornar a mensagem persistente
                headers={'sender_name': sender_name}
            )
        )
        print(f" [x] Enviado: '{msg}' de '{sender_name}'")
        # Notifica os observadores
        self.notify_observers(msg, sender_name)

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    produtor = ProdutorMensagens()
    produtor.send_message('Hello World', 'Backend')
    produtor.close()
