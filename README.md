Sistema de Gestão de Marcações Online

## Nome e objetivo

O Sistema de Gestão de Marcações é uma aplicação para gerir as marcações de um estabelecimento de serviços. Permite aos clientes consultar serviços e horários disponíveis e marcar uma consulta. Também permite ao administrador gerir os serviços e atualizar o resultado das marcações.

O sistema contabiliza as faltas de cada cliente. Ao atingir duas faltas, o cliente fica impedido de efetuar novas marcações e recebe a indicação de um contacto de WhatsApp.

## Funcionalidades previstas

- Consultar os serviços disponíveis.
- Consultar os horários disponíveis.
- Efetuar uma marcação com nome, número de telefone e email.
- Criar a marcação já confirmada, sem estado pendente.
- Consultar e gerir marcações através da área de administração.
- Atualizar o estado da marcação para **realizada**, **cancelada** ou **falta**.
- Contabilizar as faltas de cada cliente.
- Impedir novas marcações quando o cliente tiver duas faltas.

## Requisitos

- Python 3.14.5
- PostgreSQL 18.6-3-windows-x64
- Git version 2.56.0.windows.2
- Acesso ao terminal ou à linha de comandos

## Preparação do ambiente

Crie a base de dados sistema_online no PostgreSQL e execute o ficheiro data/schema.sql através do pgAdmin.

## Instalação
Crie um ficheiro .env na pasta principal do projeto:

env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sistema_online
DB_USER=postgres
DB_PASSWORD=coloque_a_sua_palavra_passe
FLASK_SECRET_KEY=coloque_uma_chave_secreta

## Comando de execução

Terminal
source .venv/Scripts/activate
export PYTHONPATH=src
python -m sistema_marcacao_online.main

Flask 
PYTHONPATH=src flask --app sistema_marcacao_online.web run --debug

## Configuração

python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
PYTHONPATH=src python -m sistema_marcacao_online.criar_admin_inicial
PYTHONPATH=src flask --app sistema_marcacao_online.web run --debug

## Comando dos testes

 PYTHONPATH=src python -m unittest discover -s test -v

## Limitações conhecidas

- A aplicação destina-se inicialmente a um único estabelecimento.
- A marcação é confirmada no momento em que é criada.
- O estado da marcação é atualizado pelo administrador para realizada, cancelada ou falta.
- O bloqueio é aplicado quando o cliente acumula duas faltas.