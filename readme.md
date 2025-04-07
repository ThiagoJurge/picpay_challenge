# 💸 PicPay Simplificado

Repositório criado para cumprir o desafio elaborado pela [PicPay](https://github.com/PicPay/picpay-desafio-backend).

---

## 🧪 Tecnologias utilizadas

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/Postgres-15-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-blue?logo=docker)

---

## ⚙️ Funcionalidades

- Cadastro de usuários (`comum` ou `lojista`)
- Criação automática de carteira ao registrar usuário
- Transferência de saldo entre carteiras
- Regras de negócio:
  - Usuáios **comuns** podem realizar qualquer tipo de transferência
  - Usuários **lojistas** podem somente receber transferências
  - Validação de saldo antes de transferir
- Histórico de transações por usuário

---

## 🧑‍💻 Como rodar o projeto

### 🔧 Pré-requisitos

- Docker

### 🚀 Rodando com Docker

1. Clone o repositório:

```bash
git clone https://github.com/ThiagoJurge/picpay_challenge
cd picpay-simplificado
docker-compose up -d
```
