import pika
import json

class ProdutorMensagens:
    QUEUE_NAME = "msg-in"
    EXCHANGE_GROUP = "clientes1-3"

    def __init__(self):
        self.factory = pika.ConnectionParameters(
            host="189.8.205.54",
            virtual_host="thanos",
            credentials=pika.PlainCredentials("senai", "senai@")
        )

    def send_message(self, msg, sender_name):
        with pika.BlockingConnection(self.factory) as connection:
            channel = connection.channel()

            channel.exchange_declare(exchange=self.EXCHANGE_GROUP, exchange_type='fanout', durable=True)

            property = pika.BasicProperties(headers={'sender_name': sender_name})

            message_body = json.dumps({
                "message": msg,
                "sender_name": sender_name
            })

            channel.basic_publish(exchange=self.EXCHANGE_GROUP, routing_key='', body=message_body.encode())
            print(f" [x] Enviado...: '{msg}' de '{sender_name}'")


if __name__ == "__main__":
    produtor = ProdutorMensagens()
    produtor.send_message("Hello World", "Backend")
