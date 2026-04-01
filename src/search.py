import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chat_models import init_chat_model   
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    
    if question is None:
        return search_prompt

    validate_config()

    embeddings = create_embeddings()
    store = create_vector_store(embeddings)

    llm = init_chat_model(
      model="gemini-2.5-flash",
      model_provider="google_genai"
    )

    results = store.similarity_search_with_score(query=question, k=10)
    prompt = create_prompt(results, question)
    response = llm.invoke(prompt)
    return response.content

def validate_config():
    required_vars = (
        "GOOGLE_API_KEY",
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
    )

    for var in required_vars:
        if not os.getenv(var):
            raise RuntimeError(f"Environment variable {var} is not set")
        
def create_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL"),
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

def create_vector_store(embeddings):
    return PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )

def create_prompt(results, question):
    context_chunks = []
    for doc, _ in results:
        context_chunks.append(doc.page_content)
    
    contexto = "\n\n".join(context_chunks)

    prompt = PROMPT_TEMPLATE.format(
        contexto = contexto,
        pergunta = question
    )

    return prompt