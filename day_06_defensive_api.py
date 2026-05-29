from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.embeddings import DeterministicFakeEmbedding

# 1. Define the Strict Input Schema using Pydantic
class SearchRequest(BaseModel):
    # Field validation ensures the query cannot be empty or just spaces
    query: str = Field(..., min_length=1, description="The semantic search string cannot be blank.")

# 2. Initialize the Web Engine
app = FastAPI(title="Hardened Vector Search API")

# 3. Setup and Index Vector DB (Simulated Knowledge Base)
print("Initializing Vector Database Engine...")
raw_knowledge_base = (
    "The primary tech stack for modern GenAI engineering focuses heavily on Python. "
    "FastAPI is utilized to build lightning-fast web endpoints, while ChromaDB serves "
    "as the core vector store for handling semantic search operations."
)

splitter = RecursiveCharacterTextSplitter(chunk_size=130, chunk_overlap=15)
chunks = splitter.split_text(raw_knowledge_base)
embedding_engine = DeterministicFakeEmbedding(size=1536)
vector_store = Chroma.from_texts(texts=chunks, embedding=embedding_engine, collection_name="hardened_collection")
print("Knowledge base successfully indexed.")

# 4. The Hardened Search Endpoint
@app.post("/api/v1/search")
def search_knowledge_base(payload: SearchRequest): # Enforcing the Pydantic class here
    # Strip whitespace to prevent malicious space-only queries ("   ")
    clean_query = payload.query.strip()
    
    if not clean_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Query validation failed: Search string cannot consist only of spaces."
        )
        
    print(f"Hardened Web Search Processing Request: '{clean_query}'")
    
    try:
        # Run the similarity search query
        matching_docs = vector_store.similarity_search(query=clean_query, k=1)
        retrieved_context = matching_docs[0].page_content if matching_docs else "No match found."
        
        return {
            "success": True,
            "status": "Processed",
            "search_query": clean_query,
            "retrieved_knowledge_chunk": retrieved_context
        }
    except Exception as e:
        # Catch-all exception handling to ensure the entire server engine never crashes out
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal database processing failure: {str(e)}"
        )