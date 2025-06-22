from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from embedding import Embedding
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

load_dotenv()

class CodeExp:
    def __init__(self, model, embedder) -> None:
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.model = model
        self.embedder = embedder

    def get_context(self, code):
        vs = self.embedder.load_vectorstore("faiss_code_index")
        context = self.embedder.search_similar_chunks(code, vs)
        return context
        
    def invoke(self, user_input, **kwargs):
        if 'context' in kwargs:
            user_input+= f"\n\nContext: {kwargs['context']}"
        else:
            user_input+= f"\n\nContext: {self.get_context(user_input)}"

        prompt_template = ChatPromptTemplate.from_template(
            """You are an expert programming assistant.

        Your task is to help the user understand code based on a given natural language prompt and relevant context chunks.

        ---

        🔍 **User Query and Context:**
        {input}

        ✅ Please **explain the code** in a **detailed**, **clear**, and **step-by-step** way that helps the user understand the logic, flow, and purpose of the code.

        Use bullet points or numbered lists where appropriate.
        You output should be straight forward and to the point. and concise.
        """
        )

        # Set up streaming handler
        handler = StreamingStdOutCallbackHandler()
        chain = prompt_template | self.model
        # Use stream method if available
        if hasattr(chain, 'stream'):
            response = ""
            for chunk in chain.stream({"input": user_input}, callbacks=[handler]):
                if hasattr(chunk, 'content'):
                    response += chunk.content
                else:
                    response += str(chunk)
            return response
        else:
            res = chain.invoke({"input": user_input})
            return res
    


# To use RAG for context:
# print(exp.invoke(user_input="what is this code about", code="def reverse(a): return a[::-1]"))

