# Items Service

Microsserviço responsável pelo cardápio do restaurante.

## Porta: `8001`

## Como rodar localmente

```bash
uv sync
uv run uvicorn main:app --reload --port 8001
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /health | Health check |
| GET | /items/ | Lista todos os itens ativos |
| POST | /items/ | Cria um item |
| GET | /items/{id}/ | Busca item por ID |
| PUT | /items/{id}/ | Atualiza item completo |
| PATCH | /items/{id}/ | Atualiza item parcial |
| DELETE | /items/{id}/ | Remove item (soft delete) |
| PATCH | /items/stock/reduce/ | Reduz estoque em bulk (uso interno do orders-service) |

## Docs interativas

Acesse `http://localhost:8001/docs` após subir o serviço.