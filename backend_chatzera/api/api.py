from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend_chatzera.server.produtor_mensagens import ProdutorMensagens

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}

class ChatMessage(BaseModel):
    message: str
    sender_name: str

@app.post('/chat')
def send_message(chat_message: ChatMessage):

    produtor = ProdutorMensagens()
    produtor.send_message(chat_message.message, chat_message.sender_name)

    return {'Mensagem enviada': chat_message.message}