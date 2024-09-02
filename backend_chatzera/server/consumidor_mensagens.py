import pika
from tkinter import messagebox, Tk
import json

class ConsumidorMensagens:
    QUEUE_NAME = "cli-1"

    def __init__(self):
        self.factory = pika.ConnectionParameters(
            host="189.8.205.54",
            virtual_host="thanos",
            credentials=pika.PlainCredentials("senai", "senai@")
        )

    def start_consuming(self):
        with pika.BlockingConnection(self.factory) as connection:
            channel = connection.channel()

            # Declara a fila com parâmetros adicionais
            args = {"x-max-length": 100}
            channel.queue_declare(queue=self.QUEUE_NAME, durable=True, arguments=args)
            print(" [*] Aguardando mensagens. Para sair, pressione CTRL+C")

            def callback(ch, method, properties, body):
                data = json.loads(body.decode("UTF-8"))
                msg = data["message"]
                sender_name = data["sender_name"]
                print(f" [!] Mensagem recebida de {sender_name}: '{msg}'")

            # Inicia o consumo de mensagens
            channel.basic_consume(queue=self.QUEUE_NAME, on_message_callback=callback, auto_ack=True)

            print(" [*] Esperando mensagens...")
            channel.start_consuming()

if __name__ == "__main__":
    consumidor = ConsumidorMensagens()
    consumidor.start_consuming()
