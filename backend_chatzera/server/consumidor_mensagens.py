import pika
from tkinter import messagebox, Tk

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
                print(f" [x] Recebido: {body}")
                msg = body.decode("UTF-8")
                print(f" [!] Mensagem recebida: '{msg}'")
                root = Tk()
                root.withdraw()  # Oculta a janela principal do Tkinter
                messagebox.showinfo("Mensagem da fila " + self.QUEUE_NAME, f" [!] Mensagem recebida : '{msg}'")
                root.destroy()

            # Inicia o consumo de mensagens
            channel.basic_consume(queue=self.QUEUE_NAME, on_message_callback=callback, auto_ack=True)

            print(" [*] Esperando mensagens...")
            channel.start_consuming()

if __name__ == "__main__":
    consumidor = ConsumidorMensagens()
    consumidor.start_consuming()
