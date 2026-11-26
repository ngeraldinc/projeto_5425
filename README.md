## Nome e objetivo

Sistema de Gestão de Marcações Online

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

- Python 3.14.5 instalado para Windows
- PostgreSQL instalado e em execução
- Git instalado
- PowerShell
- Acesso à base de dados PostgreSQL

## Preparação do ambiente

- Clone o repositório do GitHub e abra a pasta do projeto no terminal.
- Abra o pgAdmin e crie uma base de dados com o nome sistema_online.
- Abra o Query Tool ligado à base de dados sistema_online.
- Abra e execute o ficheiro data/schema.sql.
- Atualize a lista de tabelas no pgAdmin.

## Instalação

- Crie um ficheiro .env na pasta principal do projeto, ao mesmo nível de README.md e requirements.txt:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=sistema_online
DB_USER=postgres
DB_PASSWORD=coloque_a_sua_palavra_passe
FLASK_SECRET_KEY=coloque_uma_chave_secreta

Substitua DB_PASSWORD pela palavra-passe usada no PostgreSQL. O ficheiro .env contém credenciais e não deve ser enviado para o GitHub.

- Instalar dependências
Abrir o PowerShell na pasta principal do projeto e executar:

```
py -3.14 -m venv .venv-win
.\.venv-win\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

O prefixo (.venv-win) no início da linha da consola indica que o ambiente virtual está ativo. Na primeira utilização, verificar a instalação do Psycopg:

```
python -c "import psycopg; print(psycopg.__version__); print(psycopg.pq.__impl__)"
```

- Criar o administrador inicial

Com o ambiente virtual ativo:

```
$env:PYTHONPATH = "src"
python -m sistema_marcacao_online.criar_admin_inicial
```

- Executar pela consola

```
$env:PYTHONPATH = "src"
python -m sistema_marcacao_online.main
```

- Executar a aplicação Web com Flask

```
$env:PYTHONPATH = "src"
python -m flask --app sistema_marcacao_online.web run --debug
```

Aceder ao endereço indicado pelo Flask, normalmente http://127.0.0.1:5000. Para encerrar o servidor, voltar à consola e pressionar Ctrl+C.

Cada vez que abrir uma nova consola, é necessário ativar o ambiente virtual antes de executar o projeto:

```
.\.venv-win\Scripts\Activate.ps1
```  

## Comando dos testes

```
 PYTHONPATH=src python -m unittest discover -s test -v
```

## Limitações conhecidas

- A aplicação destina-se inicialmente a um único estabelecimento.
- A marcação é confirmada no momento em que é criada.
- O estado da marcação é atualizado pelo administrador para realizada, cancelada ou falta.
- O bloqueio é aplicado quando o cliente acumula duas faltas.

