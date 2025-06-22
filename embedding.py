from sentence_transformers import SentenceTransformer
import traceback
from typing import List
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_splitter import CodeChunker

class Embedding:
    def __init__(self, model, top_k: int = 3):
        self.model = model
        self.docs = []
        self.index = None
        self.top_k = top_k

    def build_vectorstore(self, documents, save_path="faiss_code_index"):
    # Load a compact and fast embedding model
        embedder = self.model

        vectorstore = FAISS.from_documents(documents, embedder)

        vectorstore.save_local(save_path)
        print(f"✅ FAISS index saved at: {save_path}")

    def load_vectorstore(self, path="faiss_code_index"):
        return FAISS.load_local(path, self.model, allow_dangerous_deserialization=True)

    def search_similar_chunks(self, query, vectorstore, top_k=None):
        if top_k is None:
             top_k = self.top_k
        results = vectorstore.similarity_search(query, k=top_k)

        return results


# # Example usage:
# if __name__ == "__main__":
#         emb = Embedding()
#         chunker = CodeChunker()
#         docs = chunker.get_code_chunks_from_directory(directory="../codebase")  # or all files

#         # Step 2: Build and save vector index
#         emb.build_vectorstore(docs, save_path="faiss_code_index")

#         # Step 3: Load and query
#         vs = emb.load_vectorstore("faiss_code_index")
#         context = emb.search_similar_chunks("optimize merge sort", vs)
