# Projeto de Chat com RabbitMQ

## Descrição do Projeto

Este é um sistema de chat desenvolvido em Python, utilizando RabbitMQ como sistema de mensageria. O sistema permite que múltiplos clientes se conectem a um servidor de chat e enviem mensagens para todos os usuários da sala. As mensagens são distribuídas pelo servidor para todos os usuários conectados à sala.

Após rodar o servidor com o Uvicorn, você pode acessar e utilizar o chat do front-end aqui: [ChatZera](https://chatzera.netlify.app/).

## Pré-requisitos

- Python 3.8+
- RabbitMQ
- FastAPI
- Uvicorn
- Pika (biblioteca Python para RabbitMQ)

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/chat_project.git
   ```
2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    ```
3. Entre no ambiente virtual

    Para Linux  

        source venv/bin/activate 

   Para Windows

        venv\Scripts\activate

4. Após entrar no ambiente virtual instale as dependencias com o comando

    pip install -r requirements.txt


## Rodando o Projeto:

1. No diretório raiz do projeto, utilize o seguinte comando para iniciar o servidor:
    ```bash
    uvicorn backend_chatzera.api.api:app --reload
    ```
2. Interaja com o cliente de chat:

Após iniciar a API, você pode interagir com o cliente de chat através das rotas expostas pelo FastAPI. Use uma ferramenta como curl, Postman, ou faça requisições via código para enviar e receber mensagens.

## Uso

- **Enviando mensagens:** Envie uma requisição POST para a rota `/send_message/` da API, incluindo o nome do responsável e a mensagem no corpo da requisição.

- **Recebendo mensagens:** As mensagens são automaticamente distribuídas e podem ser visualizadas diretamente no console onde o servidor de chat está sendo executado.
