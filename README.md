Projeto de Chat com RabbitMQ
Descrição do Projeto

Este é um projeto de um sistema de chat, desenvolvido em Python, utilizando RabbitMQ como sistema de mensageria. O sistema permite que múltiplos clientes se conectem a um servidor de chat, e enviem mensagens para todos os usuários da sala. As mensagens são distribuídas pelo servidor para todos os usuários conectados à sala.

Após rodar o servidor com o uvicorn pode acessar e utilizar usando o chat do front-end aqui **link: [ChatZera](https://chatzera.netlify.app/)**

Pré-requisitos

    Python 3.8+
    RabbitMQ
    FastAPI
    Uvicorn
    Pika (biblioteca Python para RabbitMQ)

Instalação

Clone o repositório

    git clone https://github.com/seu-usuario/chat_project.git

Crie um ambiente virtual:

    python -m venv venv

Entre no ambiente virtual
Para Linux  

    source venv/bin/activate 
Para Windows

    venv\Scripts\activate

Após entrar no ambiente virtual instale as dependencias com o comando

    pip install -r requirements.txt


Para rodar o projeto:

No diretório raiz utilize o seguinte comando:

    uvicorn backend_chatzera.api.api:app --reload

Interaja com o cliente de chat:

Após iniciar a API, você pode interagir com o cliente de chat através das rotas expostas pelo FastAPI. Use uma ferramenta como curl, Postman, ou faça requisições via código para enviar e receber mensagens.

Uso

    Enviando mensagens: Envie uma requisição POST para a rota /send_message/ da API, incluindo o nome do responsável e a mensagem no corpo da requisição.

    Recebendo mensagens: As mensagens são automaticamente distribuídas e podem ser visualizadas diretamente no console onde o servidor de chat está sendo executado.
