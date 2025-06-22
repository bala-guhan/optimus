from sub_agent import SubAgent
from langchain_core.tools import tool
from langgraph.graph import StateGraph, add_messages, START, END
from typing import Annotated, TypedDict
from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
import uuid
import json
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from embedding import Embedding
from instant_refactor import Refactor
from langchain_splitter import CodeChunker
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
import time
import warnings
import psycopg2
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv()

class OptimusPrime:
    def __init__(self, codebase: str = None) -> None:
        if not codebase:
            raise ValueError("Codebase filepath is necessary for applying accessibility! Please provide the filepath.")
        elif not os.path.exists(codebase):
            raise ValueError("You must provide a valid codebase directory path to start the agent.")
        # Centralized instance creation
        llama_chat = ChatGroq(model = "llama-3.3-70b-versatile", temperature=0.2)
        llama_ollama = self.load_ollama()
        self.embedding_model = self.load_embedding_model()
        embedder = Embedding(self.embedding_model)
        refactorer = Refactor(model=llama_chat)
        
        print("Indexing CodeBase...")
        start = time.time()
        chunker = CodeChunker()
        docs = chunker.get_code_chunks_from_directory(codebase)
        embedder.build_vectorstore(docs, save_path="faiss_code_index")
        print(f"Time Taken for Indexing CodeBase : {time.time() - start}")
        
        self.sub_agent = SubAgent(llama=llama_ollama, embedder=embedder, refactorer=refactorer)
        self.graph = None
        self.checkpointer = MemorySaver()
        self.build_graph()

    def load_ollama(self):
        start = time.time()
        print("Loading the Ollama LLM instance...")
        ollama_model = Ollama(model="llama3", base_url="http://host.docker.internal:11434")        
        end = time.time()
        print(f"Loaded the Ollama model: {end-start}")
        return ollama_model

    def load_embedding_model(self):
        start = time.time()
        print("Loading the Embedding model...")
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        end = time.time()
        print(f"Loaded the embedding model: {end-start}")
        return embedding_model

    def build_graph(self):
        class GraphState(TypedDict):
            messages: Annotated[list, add_messages]

        graph_builder = StateGraph(GraphState)

        def chatbot(state: GraphState):
            last_message = state["messages"][-1]
            response = self.sub_agent.run(last_message.content)
            # If response is a dict, convert to string
            if isinstance(response, dict):
                response = json.dumps(response, indent=2)
            return {"messages": [AIMessage(content=response)]}

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)

        self.graph = graph_builder.compile(checkpointer=self.checkpointer)

        try:
            display(Image(self.graph.get_graph().draw_mermaid_png()))
        except Exception:
            pass
        return self.graph

    def chat(self):
        session_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": session_id}}
        print("Starting chat session. Type 'exit' to end.")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break

            events = self.graph.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config,
                stream_mode="values",
            )
            for event in events:
                last_message = event["messages"][-1]
                print(f"AI: {last_message.content}")

        self.save_history(config)

    def save_history(self, config):
        db_url = os.getenv("DATABASE_URL")
        thread_state = self.checkpointer.get(config)
        if thread_state:
            print("DEBUG thread_state keys:", thread_state.keys())
            print("DEBUG channel_values:", thread_state["channel_values"])
            # return  # Remove this after debugging
            # Try to extract messages from channel_values
            channel_values = thread_state["channel_values"]
            # The structure may be: {'messages': [HumanMessage(...), AIMessage(...), ...]}
            if "messages" in channel_values:
                messages = channel_values["messages"]
                serializable_messages = [
                    {"type": msg.type, "content": msg.content} for msg in messages
                ]
                # Connect to PostgreSQL
                conn = psycopg2.connect(db_url)
                cur = conn.cursor()
                thread_id = config['configurable']['thread_id']
                for msg in serializable_messages:
                    cur.execute(
                        "INSERT INTO chat_history (thread_id, message_type, content) VALUES (%s, %s, %s)",
                        (thread_id, msg["type"], msg["content"])
                    )
                conn.commit()
                cur.close()
                conn.close()
                print(f"Chat history saved to PostgreSQL for thread {thread_id}")
            else:
                print("No 'messages' key found in channel_values:", channel_values)
        else:
            print("No chat history found for this session.")

    def show_chat_history(self, thread_id):
        import psycopg2
        import os
        db_url = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT message_type, content, created_at FROM chat_history WHERE thread_id = %s ORDER BY created_at", (thread_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if not rows:
            print(f"No chat history found for thread {thread_id}")
            return
        print(f"Chat history for thread {thread_id}:")
        for i, (msg_type, content, created_at) in enumerate(rows, 1):
            print(f"[{i}] ({created_at}) {msg_type}: {content}\n")

if __name__ == "__main__":
    import sys
    codebase_path = sys.argv[1] if len(sys.argv) > 1 else None
    agent = OptimusPrime(codebase=codebase_path)
    agent.chat()
    

    

