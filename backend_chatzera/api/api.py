from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import threading
from backend_chatzera.server.produtor_mensagens import ProdutorMensagens 
from backend_chatzera.server.consumidor_mensagens import  ConsumidorMensagens

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class ChatMessage(BaseModel):
    message: str
    sender_name: str

# Gerenciador de WebSockets
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, sender_name: str):
        for connection in self.active_connections:
            await connection.send_json({"message": message, "sender_name": sender_name})


ws_manager = WebSocketManager()

produtor = ProdutorMensagens()

def broadcast_message(msg, sender_name):
    import asyncio
    asyncio.run(send_to_all(msg, sender_name))

async def send_to_all(message: str, sender_name: str):
    await ws_manager.send_message(message, sender_name)

consumidor = ConsumidorMensagens(callback=broadcast_message)

def start_consumidor():
    consumidor.start_consuming()

consumidor_thread = threading.Thread(target=start_consumidor, daemon=True)
consumidor_thread.start()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            sender_name = data.get("sender_name")
            if message and sender_name:
                produtor.send_message(message, sender_name)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

@app.post('/chat')
def send_message(chat_message: ChatMessage):
    if chat_message.message and chat_message.sender_name:
        produtor.send_message(chat_message.message, chat_message.sender_name)
        return {'Mensagem enviada': chat_message.message}
    return {'Erro': 'Dados inválidos'}, 400
