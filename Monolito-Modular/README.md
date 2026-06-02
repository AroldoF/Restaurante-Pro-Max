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

## 🔍 Testes

| Métrica                 | Monolito         | Monolito Modular |
| ----------------------- | ---------------- | ---------------- |
| Requisições             | 500              | 500              |
| Usuários Virtuais (VUs) | 50               | 50               |
| Taxa de Sucesso         | 100%             | 100%             |
| Tempo Médio             | **454.33 ms**    | 549.25 ms        |
| Tempo Mediano           | **375.15 ms**    | 438.35 ms        |
| Tempo Mínimo            | **35.61 ms**     | 37.82 ms         |
| Tempo Máximo            | **2.53 s**       | 3.60 s           |
| P90                     | **818.34 ms**    | 991.75 ms        |
| P95                     | **1.00 s**       | 1.30 s           |
| Throughput (req/s)      | **104.23 req/s** | 81.08 req/s      |
| Tempo Total do Teste    | **4.8 s**        | 6.2 s            |
| Falhas HTTP             | 0%               | 0%               |

### Diferença percentual

| Métrica     | Diferença                               |
| ----------- | --------------------------------------- |
| Tempo Médio | Monolito ≈ **17,3% mais rápido**        |
| Throughput  | Monolito ≈ **28,6% mais requisições/s** |
| P90         | Monolito ≈ **17,5% melhor**             |
| P95         | Monolito ≈ **23% melhor**               |
| Tempo Total | Monolito ≈ **22,6% mais rápido**        |

### Análise

Os dois sistemas passaram no teste sem erros (500/500 requisições).

O Monolito apresentou melhor desempenho em todos os indicadores observados:

Menor latência média.
Menor latência nos percentis P90 e P95.
Maior throughput.
Menor duração total do teste.

Isso é esperado. Em uma aplicação modularizada existe um pequeno custo adicional causado por:

Mais camadas de abstração.
Injeção de dependências.
Separação em serviços, casos de uso e repositórios.
Mais objetos sendo instanciados durante o fluxo.

Por outro lado, a diferença observada (≈17% na média) não é grande. Considerando os ganhos de organização, manutenibilidade e escalabilidade do código, o resultado do Monolito Modular ainda é bastante próximo do monolito tradicional.
