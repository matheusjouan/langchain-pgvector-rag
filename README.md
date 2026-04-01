# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto utiliza:

* **LangChain**
* **Google Gemini**
* **PGVector (PostgreSQL)**
* **Docker**

O sistema permite consultar informações contidas em um **PDF previamente ingerido**, garantindo que as respostas sejam geradas **apenas com base no contexto armazenado no banco vetorial**.

---

# Arquitetura do Projeto

Fluxo de funcionamento:

```
PDF
 ↓
Ingestão (embeddings)
 ↓
PostgreSQL + PGVector
 ↓
Busca vetorial
 ↓
Prompt com contexto
 ↓
Gemini LLM
 ↓
Resposta ao usuário
```

---

# Estrutura do Projeto

```
.
├── docker-compose.yml
├── README.md
└── src
    ├── ingest.py
    ├── search.py
    └── chat.py
```

**Descrição dos scripts:**

* `ingest.py` → Processa o PDF e gera embeddings armazenados no PGVector
* `search.py` → Implementa a busca vetorial e construção do prompt
* `chat.py` → Interface de chat via terminal

---

# Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

* **Docker**
* **Python 3.10+**
* **pip**

Também é necessário configurar as variáveis de ambiente:

```
GOOGLE_API_KEY
DATABASE_URL
PG_VECTOR_COLLECTION_NAME
GOOGLE_EMBEDDING_MODEL
```

---

# Ordem de Execução

## 1. Subir o banco de dados

```
docker compose up -d
```

Isso iniciará um container PostgreSQL com suporte a **PGVector**.

---

## 2. Executar a ingestão do PDF

```
python src/ingest.py
```

Este passo:

* lê o PDF
* divide o conteúdo em chunks
* gera embeddings
* armazena no banco vetorial

---

## 3. Rodar o chat

```
python src/chat.py
```

O chat será iniciado no terminal:

```
Chat iniciado. Digite 'sair' para encerrar.
```

Exemplo de uso:

```
Pergunta: Qual é o tema principal do documento?

Resposta:
O documento descreve...
```

Para sair do chat:

```
sair
```

---

# Tecnologias Utilizadas

* Python
* LangChain
* Google Gemini
* PostgreSQL
* PGVector
* Docker

---

# Observações

O modelo foi instruído para **responder apenas com base no contexto recuperado** do banco vetorial.
Caso a informação não esteja presente no contexto, o sistema retorna:

```
Não tenho informações necessárias para responder sua pergunta.
```

---
