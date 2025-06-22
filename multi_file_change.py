from langchain_splitter import CodeChunker
from embedding import Embedding

chunker = CodeChunker()
embedder = Embedding()

docs = chunker.get_code_chunks_from_directory("../codebase")
embedder.build_vectorstore(docs, save_path="faiss_code_index")

class MultiFileCheck:
    def __init__(self) -> None:
        self.model = None
        
    def check_similarity(self, query: str):
        vectorstore = embedder.load_vectorstore("faiss_code_index")
        similar_chunks = embedder.search_similar_chunks(query, vectorstore)

        for chunk in similar_chunks:
            print("---"*12)
            print(chunk.page_content)
            print(chunk.metadata)
            print("---"*12)

# mul = MultiFileCheck()

# query = "how does the app authenticate a user and generate a token?"

# mul.check_similarity(query=query)
