# 🍽️ Restaurante Pro Max

Sistema de gerenciamento para restaurantes desenvolvido utilizando **FastAPI**, seguindo uma arquitetura **Monolítica Tradicional**, com foco na simplicidade de implementação e centralização da lógica da aplicação.

---

# 🚀 Tecnologias

- Python 3.13+
- FastAPI
- SQLModel
- SQLite
- UV
- Docker
- Docker Compose
- Swagger/OpenAPI

---

# 🏗️ Arquitetura

Esta implementação utiliza uma arquitetura **Monolítica Tradicional**.

Toda a aplicação está organizada dentro de um único sistema, compartilhando:

- Modelos
- Serviços
- Repositórios
- Banco de dados
- Dependências

Embora exista separação em camadas, os módulos possuem maior acoplamento entre si quando comparados à versão Monólito Modular.

---

# ⚠️ Diferenças para a versão Monólito Modular

Nesta versão:

❌ Não foram implementadas interfaces entre módulos.

❌ Não existe uma camada de contratos públicos.

❌ Um serviço pode depender diretamente de outro serviço.

❌ O acoplamento entre domínios é maior.

---

# 📖 Documentação da API

Após iniciar a aplicação:

## Swagger UI

```text
http://localhost:8000/docs
```

## ReDoc

```text
http://localhost:8000/redoc
```

---


# ▶️ Executando com UV

## Instalar dependências

```bash
uv sync
```

## Executar aplicação

```bash
uv run fastapi dev main.py
```

Aplicação disponível em:

```text
http://localhost:8000
```

---

# 🐳 Executando com Docker Compose

## Subir aplicação

```bash
docker compose up --build
```

## Executar em background

```bash
docker compose up -d --build
```

## Parar aplicação

```bash
docker compose down
```

---

# 🧪 Práticas adotadas

Apesar de ser uma implementação monolítica tradicional, algumas boas práticas foram mantidas:

- Separação em camadas
- Repository Pattern
- Service Layer
- Injeção de dependências do FastAPI
- Validação com Pydantic/SQLModel
- Organização por domínio

---

## 🎯 Objetivo

Esta versão existe para demonstrar uma arquitetura monolítica tradicional e servir como base de comparação.

Os principais pontos avaliados são:

- Acoplamento
- Manutenibilidade
- Escalabilidade
- Evolução para microsserviços
- Reutilização de código
- Organização dos domínios

---

## 🔍 Comparação Rápida

| Característica | Monolítico | Monólito Modular |
|---------------|------------|------------------|
| Separação por domínio | ✅ | ✅ |
| Camada de serviços | ✅ | ✅ |
| Interfaces entre módulos | ❌ | ✅ |
| Contratos públicos | ❌ | ✅ |
| Baixo acoplamento | ❌ | ✅ |
| Evolução para microsserviços | ⚠️ Mais difícil | ✅ Mais simples |
| Dependência de abstrações | ❌ | ✅ |
