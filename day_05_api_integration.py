from fastapi import FastAPI, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.embeddings import DeterministicFakeEmbedding

# 1. Initialize the FastAPI Web Engine
app = FastAPI(title="Live Vector Search API")

# 2. Setup and Index the Vector Database (Runs once when the server boots up)
print("Initializing Vector Database Engine...")
raw_knowledge_base = (
    "The primary tech stack for modern GenAI engineering focuses heavily on Python. "
    "FastAPI is utilized to build lightning-fast web endpoints, while ChromaDB serves "
    "as the core vector store for handling semantic search operations.\n\n"
    "To deploy AI applications effectively, developers leverage automation frameworks "
    "like LangChain or n8n to connect databases directly to language models."
)

# Split the raw data into clean chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=130, chunk_overlap=15)
chunks = splitter.split_text(raw_knowledge_base)

# Spin up our fake embedding encoder and populate our in-memory ChromaDB instance
embedding_engine = DeterministicFakeEmbedding(size=1536)
vector_store = Chroma.from_texts(
    texts=chunks,
    embedding=embedding_engine,
    collection_name="integration_collection"
)
print("Knowledge base successfully indexed. Server is ready to handle traffic.")

# 3. The Live Search Endpoint
@app.post("/api/v1/search")
def search_knowledge_base(payload: dict):
    # Safely extract the query string from the incoming JSON payload
    user_query = payload.get("query", "").strip()
    
    # Anti-Comfort Check: If the user sends an empty string, throw a clean error
    if not user_query:
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")
        
    print(f"Incoming Web Search Request: '{user_query}'")
    
    # Run the semantic similarity calculation against our database
    # k=1 pulls the single absolute best contextual paragraph matching the meaning
    matching_docs = vector_store.similarity_search(query=user_query, k=1)
    
    # Extract the string text from the retrieved document object
    retrieved_context = matching_docs[0].page_content if matching_docs else "No match found."
    
    # Return the clean, structured JSON response back to the internet browser
    return {
        "success": True,
        "search_query": user_query,
        "retrieved_knowledge_chunk": retrieved_context
    }