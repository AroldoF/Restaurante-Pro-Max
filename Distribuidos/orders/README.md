# Orders Service

Microsserviço responsável pelos pedidos do restaurante.

## Porta: `8002`

## Dependências

Precisa que o **items-service** esteja rodando na porta `8001`.

## Como rodar localmente

```bash
uv sync
uv run uvicorn main:app --reload --port 8002
```

## Como rodar com Docker

```bash
docker build -t orders-service .
docker run -p 8002:8002 orders-service
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /health | Health check |
| GET | /orders/ | Lista todos os pedidos |
| POST | /orders/ | Cria um pedido |
| GET | /orders/{id}/ | Busca pedido por ID |
| GET | /orders/{id}/items/ | Lista itens do pedido |
| DELETE | /orders/{id}/ | Cancela um pedido |
| PATCH | /orders/{id}/finish/ | Finaliza pedido (uso interno do payments-service) |

## Docs interativas

Acesse `http://localhost:8002/docs` após subir o serviço.