from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from ast_mapping import EXTENSION_LANGUAGE_MAP
from langchain.text_splitter import Language
# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.schema import Document

class CodeChunker:
    def __init__(self) -> None:
        self.EXTENSION_LANGUAGE_MAP = EXTENSION_LANGUAGE_MAP

    def get_line_range(self, full_text, chunk_text):
        """Estimate the start and end line numbers of a chunk."""
        start_char_index = full_text.find(chunk_text)
        if start_char_index == -1:
            return -1, -1  # fallback
        start_line = full_text[:start_char_index].count("\n") + 1
        chunk_lines = chunk_text.count("\n")
        end_line = start_line + chunk_lines
        return start_line, end_line

    def load_and_chunk_single_file(self, file_path):
        """Chunk a single code file and attach metadata (line numbers, path)."""
        file_path = Path(file_path)
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"{file_path} does not exist or is not a file")

        try:
            code = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []

        # Choose language dynamically based on extension
        ext = file_path.suffix.lower()
        if ext in self.EXTENSION_LANGUAGE_MAP:
            language = self.EXTENSION_LANGUAGE_MAP.get(ext)
        else:
            language = "NOT_FOUND"

        if language == "NOT_FOUND":
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=512, 
                chunk_overlap=64
            )
        else:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=language,
                chunk_size=512,
                chunk_overlap=64,
            )

        chunks = splitter.create_documents([code])
        for i, chunk in enumerate(chunks):
            start_line, end_line = self.get_line_range(code, chunk.page_content)
            chunk.metadata = {
                "source_file": str(file_path.resolve()),
                "chunk_index": i,
                "start_line": start_line,
                "end_line": end_line,
            }

        return chunks

    def get_code_chunks_from_directory(self, directory, chunk_size=512, chunk_overlap=64):
        """
        Recursively find all files with supported extensions in the directory,
        chunk them, and return a list of all code chunks.
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        all_chunks = []
        supported_exts = set(self.EXTENSION_LANGUAGE_MAP.keys())
        for file_path in directory.rglob('*'):
            if file_path.suffix in supported_exts and file_path.is_file():
                try:
                    # Pass chunk_size and chunk_overlap to the single file chunker
                    chunks = self.load_and_chunk_single_file(
                        file_path
                    )
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")
        return all_chunks

# chunker = CodeChunker()
# chunks = chunker.get_code_chunks_from_directory("../codebase/")

# with open("chunks.txt", 'w') as file:
#     for chunk in chunks:
#         file.write(chunk.page_content)
#         file.write(str(chunk.metadata))
#         file.write("\n")
#         file.write("---"*100)
#         file.write("\n")
