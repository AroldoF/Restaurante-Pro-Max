# Sistema de Microsserviços para Restaurante

Este repositório unifica os quatro microsserviços responsáveis pela operação do restaurante: **Items Service**, **Orders Service**, **Payment Service** e **Notification Service**.

---

## 📌 Visão Geral do Sistema e Portas

Abaixo está a matriz de portas, dependências e links de documentação interativa (Swagger) para cada serviço:

| Microsserviço | Porta | Dependência Direta | Docs Interativas (Swagger) |
| :--- | :---: | :--- | :--- |
| **Items Service** | `8001` | Nenhuma | http://localhost:8001/docs |
| **Orders Service** | `8002` | `items-service` (`8001`) | http://localhost:8002/docs |
| **Payment Service** | `8009` | RabbitMQ | http://localhost:8009/docs |
| **Notification Service** | `8010` | RabbitMQ | http://localhost:8010/docs |

---

## ▶️ Executar

* **Com Docker Compose:**
```bash
    docker compose up --build 
```

---

## 🛠️ Infraestrutura Global (Mensageria)

Os microsserviços de **Payment** e **Notification** utilizam o RabbitMQ para comunicação assíncrona. Suba a instância do mensageiro antes de iniciar estes serviços.

```bash
docker run -d --name meu-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### 1. Items Service (`Porta 8001`)
Microsserviço responsável pelos itens do restaurante.

#### Como Executar
* **Localmente:**
```bash
    uv sync
    uv run uvicorn main:app --reload --port 8001
```

* **Com Docker:**
```bash
    docker build -t items-service .
    docker run -p 8001:8001 items-service
```

#### Endpoints
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| GET | `/health` | Health check |
| GET | `/items/` | Lista todos os itens ativos |
| POST | `/items/` | Cria um item |
| GET | `/items/{id}/` | Busca item por ID |
| PUT | `/items/{id}/` | Atualiza item completo |
| PATCH | `/items/{id}/` | Atualiza item parcial |
| DELETE | `/items/{id}/` | Remove item (soft delete) |
| PATCH | `/items/stock/reduce/` | Reduz estoque em bulk (*uso interno do orders-service*) |

---

### 2. Orders Service (`Porta 8002`)
Microsserviço responsável pelos pedidos do restaurante.

ℹ️ **Aviso:** Precisa que o `items-service` esteja rodando na porta `8001`.

#### Como Executar
* **Localmente:**
```bash
    uv sync
    uv run uvicorn main:app --reload --port 8002
```

* **Com Docker:**
```bash
    docker build -t orders-service .
    docker run -p 8002:8002 orders-service
```

#### Endpoints
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| GET | `/health` | Health check |
| GET | `/orders/` | Lista todos os pedidos |
| POST | `/orders/` | Cria um pedido |
| GET | `/orders/{id}/` | Busca pedido por ID |
| GET | `/orders/{id}/items/` | Lista itens do pedido |
| DELETE | `/orders/{id}/` | Cancela um pedido |
| PATCH | `/orders/{id}/finish/` | Finaliza pedido (*uso interno do payments-service*) |

---

### 3. Payment Service (`Porta 8009`)
Microsserviço responsável pelo pagamento dos pedidos do restaurante.

ℹ️ **Aviso:** Precisa que o `orders-service` esteja rodando na porta `8002` para pegar o valor do pedido.

#### Como Executar
* **Localmente:**
```bash
    uv sync
    uv run uvicorn main:app --reload --port 8009
```

* **Com Docker:**
```bash
    docker build -t payment-service .
    docker run -p 8009:8009 payment-service
```

#### Endpoints
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| GET | `/payments/` | Lista todos os pagamentos |
| POST | `/payments/` | Cria um pagamento |
| POST | `/payments/{id}/confirm/` | Confirma um pagamento |
| GET | `/payments/{id}/` | Busca pagamento por ID |

---

### 4. Notification Service (`Porta 8010`)
Microsserviço responsável pelo recebimento das notificações e alertas dos pedidos.

#### Ações via mensageria
O sistema consome as mensagens publicadas referente ao pagamento de um pedido e cria a notificação correspondente[cite: 2].

#### Como Executar
* **Localmente:**
```bash
    uv sync
    uv run uvicorn main:app --reload --port 8010
```

* **Com Docker:**
```bash
    docker build -t notification-service .
    docker run -p 8010:8010 notification-service
```

#### Endpoints
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| GET | `/notifications/` | Lista todas as notificações de pedidos |
| GET | `/notifications/{id}/` | Busca notificação por ID |
