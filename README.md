# Desafio Luizalabs - Banking API — Python & FastAPI

API REST assíncrona para operações bancárias, desenvolvida com **Python e FastAPI**.

O projeto permite gerenciar contas e transações financeiras, com suporte a **depósitos, saques, consulta de extrato, autenticação JWT e validação de saldo**. Os dados são persistidos em **PostgreSQL**, com controle de migrations através do **Alembic**.

Projeto desenvolvido durante o bootcamp **Luizalabs — Back-end com Python**, com foco na aplicação prática de conceitos de desenvolvimento back-end e APIs REST.

## Tecnologias

* Python 3.11
* FastAPI
* PostgreSQL
* Alembic
* JWT
* bcrypt
* Pydantic
* Uvicorn
* Poetry
* OpenAPI / Swagger

## Funcionalidades

* Autenticação de usuários com JWT
* Criação e consulta de contas bancárias
* Registro de depósitos
* Registro de saques
* Consulta do histórico de transações
* Atualização automática do saldo da conta
* Bloqueio de saques quando o saldo é insuficiente
* Validação dos dados de entrada
* Persistência em PostgreSQL
* Migrations de banco de dados com Alembic
* Documentação interativa com Swagger/OpenAPI

## Regras de negócio

A API aplica validações durante as operações financeiras.

Um depósito válido aumenta o saldo da conta.

Um saque válido reduz o saldo disponível.

Caso o valor solicitado para saque seja superior ao saldo da conta, a operação é recusada e a transação não é persistida.

Exemplo:

```text
Saldo inicial:   R$ 0,00
Depósito:       +R$ 2,00
Saque:          -R$ 1,00
Saldo final:     R$ 1,00
```

Uma tentativa posterior de saque de R$ 10,00, por exemplo, é recusada por saldo insuficiente.

## Estrutura principal

```text
src/
├── controllers/
├── models/
├── schemas/
├── services/
├── database.py
├── security.py
└── main.py

migrations/
└── versions/
```

A aplicação separa responsabilidades entre controllers, schemas, modelos, serviços, configuração de banco de dados e segurança.

## Configuração do ambiente

### Pré-requisitos

* Python 3.11
* Poetry
* PostgreSQL

Clone o repositório:

```bash
git clone https://github.com/DanSouzafs/Luizalabs-desafio.git
cd Luizalabs-desafio
```

Instale as dependências:

```bash
poetry install --no-root
```

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Configure as variáveis de ambiente:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/bank_db
ENVIRONMENT=production

JWT_SECRET=sua-chave-secreta
JWT_ALGORITHM=HS256
JWT_AUDIENCE=desafio-bank
JWT_EXPIRATION_MINUTES=30
```

> Nunca envie o arquivo `.env` ou chaves reais para o repositório.

## Banco de dados

Depois de criar o banco PostgreSQL, aplique as migrations:

```bash
poetry run alembic upgrade head
```

As principais tabelas utilizadas são:

* `users`
* `accounts`
* `transactions`
* `alembic_version`

## Executando a aplicação

```bash
poetry run uvicorn src.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

## Swagger / OpenAPI

Com a aplicação em execução, acesse:

```text
http://127.0.0.1:8000/docs
```

A documentação permite explorar e testar os endpoints diretamente pelo navegador.

## Fluxo de autenticação

O endpoint:

```text
POST /auth/login
```

recebe as credenciais do usuário e retorna um `access_token` JWT.

Exemplo:

```json
{
  "username": "usuario",
  "password": "senha"
}
```

As rotas protegidas utilizam o header:

```text
Authorization: Bearer <access_token>
```

## Exemplo de transação

### Depósito

```json
{
  "account_id": 2,
  "type": "deposit",
  "amount": 2.00
}
```

### Saque

```json
{
  "account_id": 2,
  "type": "withdrawal",
  "amount": 1.00
}
```

O saldo é atualizado após cada operação válida e as transações ficam registradas no PostgreSQL.

## Endpoints principais

```text
POST /auth/login

GET  /accounts/
POST /accounts/
GET  /accounts/{id}/transactions

POST /transactions/
```

## Objetivo do projeto

Este projeto foi desenvolvido para consolidar conhecimentos em:

* desenvolvimento de APIs REST com FastAPI;
* programação assíncrona;
* autenticação e autorização;
* modelagem e persistência de dados;
* regras de negócio;
* integração com PostgreSQL;
* migrations;
* documentação de APIs.

O foco foi transformar os conceitos estudados no bootcamp em uma aplicação back-end funcional e executável.

## Autor

**Daniel Ferreira**

Projeto desenvolvido como parte da formação **Luizalabs — Back-end com Python / DIO**.
