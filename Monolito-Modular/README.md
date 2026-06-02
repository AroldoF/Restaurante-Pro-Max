# 🍽️ Restaurante Pro Max

Sistema de gerenciamento para restaurantes desenvolvido utilizando **FastAPI**, seguindo a arquitetura de **Monólito Modular**, com foco em desacoplamento, manutenção e evolução gradual para microsserviços.

---

## 🚀 Tecnologias

- Python 3.13+
- FastAPI
- SQLModel
- SQLite (desenvolvimento)
- UV (gerenciador de dependências)
- Docker
- Docker Compose
- Swagger/OpenAPI

---

## 🏗️ Arquitetura

O projeto segue o padrão de **Monólito Modular**.

Cada módulo possui sua própria responsabilidade de negócio e se comunica com outros módulos apenas através de:

- Interfaces públicas
- Serviços públicos
- Contratos bem definidos

---

### Regras da arquitetura

✅ Um módulo não acessa diretamente os modelos internos de outro módulo.

✅ Um módulo não acessa diretamente os repositórios de outro módulo.

✅ A comunicação ocorre apenas por interfaces públicas.

✅ Cada módulo é responsável por suas próprias regras de negócio.

✅ Dependências sempre apontam para contratos e abstrações.

---

## 📖 Documentação da API

Após iniciar a aplicação:

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

## ▶️ Executando com UV

### Instalar dependências

```bash
uv sync
```

### Iniciar aplicação

```bash
uv run fastapi dev main.py
```

Aplicação disponível em:

```text
http://localhost:8000
```

---

## 🐳 Executando com Docker Compose

### Subir aplicação

```bash
docker compose up --build
```

### Executar em background

```bash
docker compose up -d --build
```

### Parar aplicação

```bash
docker compose down
```

---

## 🎯 Objetivo

O Restaurante Pro Max foi projetado para demonstrar uma aplicação FastAPI organizada utilizando Monólito Modular, permitindo crescimento sustentável e uma futura migração para microsserviços sem grandes alterações nas regras de negócio.

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
