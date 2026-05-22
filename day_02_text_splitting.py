import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def ingest_and_split_document(file_path: str):

    # 1 . standard python file handling: read the raw text file
    if not os.path.exists(file_path):
       print(f"Error: The file '{file_path }' does not exist.")
       return
    
    with open(file_path, "r", encoding="utf-8") as file:
        raw_text = file.read()

    print(f" Successfully loaded file. Total characters: {len(raw_text)}\n")

    # 2.Initalize the smart splitter
    # It recursively tries to split by paragraphs (\n\n), sentences (\n), spaces (" "), and characters ("")
    # sequentially to keep sentences and paragraphs intact as much as possible.

    splitter = RecursiveCharacterTextSplitter (
        chunk_size=150,  # Max characters per chunk
        chunk_overlap=20   # Overlap buffer between consecutive chunks
    )

    # 3. Execute the splitting action
    chunks = splitter.split_text(raw_text)

    #4. inspect the output arrays
    print(f"Split text into {len(chunks)} distinct chunks.\n")

    for index, chunk in enumerate(chunks):
        print(f"--- Chunk {index + 1} ---")
        print(chunk)
        print(f"Length: {len(chunk)} characters\n")

if __name__ == "__main__":
    # run the ingestion fucntion on our sample file
    ingest_and_split_document("data_source.txt")