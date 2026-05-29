import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# 1. Input Contract Enforcement (Restored Pydantic Class)
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The user question cannot be blank.")

# 2. Initialize App Gateway
app = FastAPI(title="Complete End-to-End RAG Engine")

# 3. Spin Up Data Store Layer
print("Building Local Vector Memory Store...")
knowledge_base = (
    "The primary tech stack for modern GenAI engineering focuses heavily on Python. "
    "FastAPI is utilized to build lightning-fast web endpoints, while ChromaDB serves "
    "as the core vector store for handling semantic search operations."
)

splitter = RecursiveCharacterTextSplitter(chunk_size=130, chunk_overlap=15)
chunks = splitter.split_text(knowledge_base)
embedding_engine = DeterministicFakeEmbedding(size=1536)
vector_store = Chroma.from_texts(texts=chunks, embedding=embedding_engine, collection_name="final_rag_collection")
print("Vector Store Loaded and Indexed.")

# 4. Initialize LLM Gateway with defensive fallback
gemini_key = os.getenv("GEMINI_API_KEY")

if gemini_key:
    from langchain_google_genai import ChatGoogleGenerativeAI
    # Swapped to gemini-3.5-flash because 1.5 is officially deprecated by Google
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0, google_api_key=gemini_key)
    print("Live Gemini API Gateway connected successfully!")
else:
    # Manual backup slot
    manual_key = "" 
    
    if manual_key and manual_key != "PASTE_YOUR_AIZA_KEY_HERE":
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0, google_api_key=manual_key)
        print("Live Gemini API Gateway connected via manual key entry!")
    else:
        from langchain_core.language_models import FakeListChatModel
        llm = FakeListChatModel(responses=["[Mock Response] Please provide a GEMINI_API_KEY to see dynamic AI answers."])
        print("Running with Mock LLM Engine Fallback (No Gemini API Key found).")

# 5. Define the Structural RAG Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an elite backend GenAI assistant. Answer the user's question using ONLY the provided context blocks. If you do not know, say you don't know.\n\nContext:\n{context}"),
    ("human", "{question}")
])

# 6. The Grand Finale RAG Endpoint (Fixed Validation Logic)
@app.post("/api/v1/chat")
def generate_rag_response(payload: ChatRequest):
    clean_query = payload.question.strip()
    
    if not clean_query:
        raise HTTPException(status_code=400, detail="Question cannot be empty spaces.")
        
    print(f"RAG Pipeline Engaged: Processing '{clean_query}'")
    
    try:
        # Step A: Retrieve the Context Block from ChromaDB
        matching_docs = vector_store.similarity_search(query=clean_query, k=1)
        context_chunk = matching_docs[0].page_content if matching_docs else "No context found."
        print(f"Context Retrieved from ChromaDB: '{context_chunk[:40]}...'")
        
        # Step B: Format the prompt instructions
        formatted_prompt = prompt_template.format(context=context_chunk, question=clean_query)
        
        # Step C: Stream to the LLM and get the structured answer
        ai_response = llm.invoke(formatted_prompt)
        
        # Pull text string response safely regardless of LangChain model type
        final_answer = ai_response.content if hasattr(ai_response, 'content') else str(ai_response)
        
        return {
            "success": True,
            "engine": "RAG-Pipeline-v1",
            "user_question": clean_query,
            "retrieved_context": context_chunk,
            "llm_generated_answer": final_answer
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline breakdown: {str(e)}"
        )