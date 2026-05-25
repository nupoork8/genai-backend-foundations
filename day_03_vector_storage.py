from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.embeddings import DeterministicFakeEmbedding

def run_vector_search_pipeline():
    # 1. Raw Text Source Data
    raw_document = (
        "Retrieval-Augmented Generation (RAG) optimizes LLM outputs. "
        "It queries an external knowledge database before responding to limit hallucinations.\n\n"
        "Vector databases like ChromaDB or FAISS store these text chunks as dense "
        "mathematical arrays for rapid semantic search execution pathways.\n\n"
        "Python remains the dominant language for building GenAI backend plumbing "
        "due to robust automation packages like LangChain and FastAPI frameworks."
    )
    print("Step 1: Raw data source loaded.")

    # 2. Text Splitting (Day 2 Logic)

    splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=15)
    chunks = splitter.split_text(raw_document)
    print(f"Step 2: Text split into {len(chunks)} chunks.")

    # 3. Initialize the Vector Embedding Engine (Simulating 1536 dimensions like OpenAI)
    
    embedding_engine = DeterministicFakeEmbedding(size=1536)
    print("Step 3: Local semantic embedding engine initialized.")

    # 4. Create an In-Memory Chroma Vector Store
    # We pass the text chunks and our embedding engine. Chroma automatically calls 
    # embed_documents() under the hood to generate and index the vector arrays.

    print("Step 4: Indexing chunks into ChromaDB vector store...")
    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_engine,
        collection_name="sprint_collection"
    )
    print("Vector database successfully constructed.")

    # 5. Perform a Semantic Search Query
    
    user_query = "What programming language is used for AI backend code?"
    print(f"\n Querying database for: '{user_query}'")
    
    # Retrieve the top 1 closest semantic match (k=1)
    search_results = vector_store.similarity_search(query=user_query, k=1)

    # 6. Output the Retrieved Data Context
    print("\n--- Top Retrieved Context Document ---")
    for index, doc in enumerate(search_results):
        print(doc.page_content)
    print("-----------------------------------------\n")

if __name__ == "__main__":
    run_vector_search_pipeline()