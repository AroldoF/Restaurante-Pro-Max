# Payment Service

Microsserviço responsável pelo pagamento dos pedidos do restaurante.

## Como executar 

### Mensageria

```bash
docker run -d --name meu-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### Serviço - Porta: `8009`

#### Executar localmente

```bash
uv sync
uv run uvicorn main:app --reload --port 8009
```

#### Executar com Docker

```bash
docker build -t payment-service .
docker run -p 8009:8009 payment-service
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /payments/ | Lista todos os pagamentos |
| POST | /payments/ | Cria um pagamento |
| POST | /payments{id}/confirm/ | Confirma um pagamento |
| GET | /payments/{id}/ | Busca pagamento por ID |

## Docs interativas

Acesse `http://localhost:8009/docs` após subir o serviço.
