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
├── requirements.txt
├── .env.example
├── src/
│   ├── ingest.py
│   ├── search.py
│   └── chat.py
├── document.pdf
└── README.md
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

Também é necessário configurar as variáveis de ambiente conforme descrito no passo 3 da seção **Ordem de Execução**.

As variáveis do projeto são:

| Variável | Descrição | Valor padrão |
|---|---|---|
| `GOOGLE_API_KEY` | Chave da API do Google Gemini | *(preencher com sua chave)* |
| `GOOGLE_EMBEDDING_MODEL` | Modelo de embeddings | `models/gemini-embedding-001` |
| `DATABASE_URL` | String de conexão com o PostgreSQL | `postgresql+psycopg://postgres:postgres@localhost:5432/rag` |
| `PG_VECTOR_COLLECTION_NAME` | Nome da collection no PGVector | `rag_documents` |
| `PDF_PATH` | Caminho do PDF para ingestão | `document.pdf` |

> **Nota:** As variáveis `DATABASE_URL`, `PG_VECTOR_COLLECTION_NAME` e `PDF_PATH` já possuem valores padrão compatíveis com o `docker-compose.yml` do projeto. Basta preencher a `GOOGLE_API_KEY` com sua chave.

> **Importante:** O arquivo `document.pdf` deve estar na raiz do projeto antes de executar a ingestão.

---

# Ordem de Execução

## 1. Criar e ativar o ambiente virtual

```bash
python -m venv venv
```

Ativar no **Linux/Mac**:

```bash
source venv/bin/activate
```

Ativar no **Windows**:

```bash
venv\Scripts\activate
```

## 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 3. Configurar as variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env` e preencha a `GOOGLE_API_KEY` com sua chave. As demais variáveis já possuem valores padrão.

## 4. Subir o banco de dados

```
docker compose up -d
```

Isso iniciará um container PostgreSQL com suporte a **PGVector**.

---

## 5. Executar a ingestão do PDF

```
python src/ingest.py
```

Este passo:

* lê o PDF
* divide o conteúdo em chunks
* gera embeddings
* armazena no banco vetorial

---

## 6. Rodar o chat

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
