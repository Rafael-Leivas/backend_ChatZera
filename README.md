README - Projeto de Chat com RabbitMQ
Descrição do Projeto

Este é um projeto de um sistema de chat, desenvolvido em Python, utilizando RabbitMQ como sistema de mensageria. O sistema permite que múltiplos clientes se conectem a um servidor de chat, escolham uma sala de comunicação, e enviem mensagens para todos os usuários da sala ou para um usuário específico. As mensagens são distribuídas pelo servidor para todos os usuários conectados à sala.

Pré-requisitos

    Python 3.8+
    RabbitMQ
    FastAPI
    Uvicorn
    Pika (biblioteca Python para RabbitMQ)

Instalação

Clone o repositório

    git clone https://github.com/seu-usuario/chat_project.git

Crie um ambiente virtual e instale as dependências:

    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    pip install -r requirements.txt

Instale e configure o RabbitMQ:

Baixe e instale o RabbitMQ seguindo as instruções no site oficial.
Após a instalação, inicie o serviço do RabbitMQ.

    Configuração do RabbitMQ:
        No arquivo server/message_broker.py, configure as credenciais e o host do RabbitMQ conforme a sua instalação.

Execução

Inicie o servidor de chat:

    Navegue até a pasta server/ e execute o servidor:

python chat_server.py

Inicie a API FastAPI:

Navegue até a pasta api/ e execute o servidor FastAPI usando o Uvicorn:

    uvicorn api:app --reload

Interaja com o cliente de chat:

Após iniciar a API, você pode interagir com o cliente de chat através das rotas expostas pelo FastAPI. Use uma ferramenta como curl, Postman, ou faça requisições via código para enviar e receber mensagens.

Uso

    Enviando mensagens: Envie uma requisição POST para a rota /send_message/ da API, incluindo o nome do responsável e a mensagem no corpo da requisição.

    Recebendo mensagens: As mensagens são automaticamente distribuídas e podem ser visualizadas diretamente no console onde o servidor de chat está sendo executado.
