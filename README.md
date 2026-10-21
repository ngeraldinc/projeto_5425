Sistema de Gestão de Marcações Online

## Nome e objetivo

O Sistema de Gestão de Marcações é uma aplicação para gerir as marcações de um estabelecimento de serviços. Permite aos clientes consultar serviços e horários disponíveis e marcar uma consulta. Também permite ao administrador gerir os serviços e atualizar o resultado das marcações.

O sistema contabiliza as faltas de cada cliente. Ao atingir duas faltas, o cliente fica impedido de efetuar novas marcações e recebe a indicação de um contacto de WhatsApp.

## Funcionalidades implementadas

- Consultar os serviços disponíveis.
- Consultar os horários disponíveis.
- Efetuar uma marcação com nome, número de telefone e email.
- Criar a marcação já confirmada, sem estado pendente.
- Consultar e gerir marcações através da área de administração.
- Atualizar o estado da marcação para **realizada**, **cancelada** ou **falta**.
- Contabilizar as faltas de cada cliente.
- Impedir novas marcações quando o cliente tiver duas faltas.
- Apresentar o contacto de WhatsApp da administração quando o cliente estiver bloqueado.


## Requisitos

- Python 3.14.5
- PostgreSQL []
- Git version 2.56.0.windows.2
- Acesso ao terminal ou à linha de comandos

## Preparação do ambiente


## Instalação


## Comando de execução


## Configuração

## Comando dos testes


## Limitações conhecidas

- A aplicação destina-se inicialmente a um único estabelecimento.
- O contacto por WhatsApp é apresentado ao cliente; o sistema não envia mensagens automaticamente.
- Não são realizados pagamentos online.
- A marcação é confirmada no momento em que é criada.
- O estado da marcação é atualizado pelo administrador para realizada, cancelada ou falta.
- O bloqueio é aplicado quando o cliente acumula duas faltas.