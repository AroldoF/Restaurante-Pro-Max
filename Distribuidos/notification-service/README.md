# Notification Service

Microsserviço responsável pelo recebimento dos pedidos.

## Como executar 

### Mensageria

```bash
docker run -d --name meu-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### Serviço - Porta: `8010`

#### Executar localmente

```bash
uv sync
uv run uvicorn main:app --reload --port 8010
```

#### Executar com Docker

```bash
docker build -t notification-service .
docker run -p 8010:8010 notification-service
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /notifications/ | Lista todas as notificações de pedidos |
| GET | /notifications/{id}/ | Busca notificação por ID |

## Ações via mensageria

O sistema consome as mensagens publicadas referente ao pagamento de um pedido e cria a notificação. 

## Docs interativas

Acesse `http://localhost:8010/docs` após subir o serviço.
