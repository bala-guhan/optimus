from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, Literal
from IPython.display import Image, display
from langchain_core.prompts import ChatPromptTemplate
from codexp_chain import CodeExp # code explanation Chain
from embedding import Embedding
from langchain_splitter import CodeChunker
import time
from pydantic import BaseModel, Field
from instant_refactor import Refactor
from langchain_community.llms import Ollama
from langgraph.graph.message import add_messages
from typing import Annotated
import os


class SubAgent:
    def __init__(self, llama, embedder, refactorer):
        self.llama = llama
        self.refactorer = refactorer
        self.embedder = embedder
        self.code_explainer = CodeExp(model=self.llama, embedder=self.embedder)
        self.graph = None
        self.build_graph()

    def build_graph(self):
        class GraphState(TypedDict):
            input: str
            task_type: Literal["explain", "refactor", "code_search"]
            result: str
            messages: Annotated[list, add_messages]

        class FileName(BaseModel):
            filename : str

        import re

        def decision_node(state: GraphState) -> GraphState:
            text = state['input']
            prompt_template = ChatPromptTemplate.from_template("""
                You are a helpful assistant. Based on the given input, you have to make a decision if it is a 
                - Code explanation task (only deals with explaining some piece of code)
                - Code refactoring (involves code analysis, code generation and replacement)
                - Code search (user wants to search for code or code snippets)

                user_input : {user_input}
                Output ONLY one of: <explain>, <refactor>, <code_search>
            """)
            chain = prompt_template | self.llama
            decision = chain.invoke({"user_input" : text})

            # Extract the keyword using regex
            match = re.search(r"<(explain|refactor|code_search)>", decision.lower())
            if match:
                state['task_type'] = match.group(1)
            else:
                state['task_type'] = 'explain'  # fallback

            state["messages"].append(f"Decision made : {state['task_type']}")
            return state

        ### 2. Decision function 
        def decide_task(state: GraphState) -> Literal["explain", "refactor", "code_search"]:
            return state["task_type"]

        def code_search_node(state: GraphState) -> GraphState:
            query = state["input"]

            vs = self.embedder.load_vectorstore("faiss_code_index")
            search_results = self.embedder.search_similar_chunks(query, vs)
            
            similar_code = ""
            for doc in search_results:
                similar_code += f"Code:\n{doc.page_content}\n"
                similar_code += f"Metadata: {doc.metadata}\n\n"

            prompt_template = ChatPromptTemplate.from_template("""
            You are a helpful assistant, who searches for a certain piece of code according to the user's input.
            Provide the user query, and the semantically parsed similar items here through similarity search.

            User Query: {query}

            Search Results:
            {similar_code}

            Provide a proper explanation of the found output considering the user's query.
            """)
            chain = prompt_template | self.llama
            result = chain.invoke({"query": query, "similar_code": similar_code})

            return {**state, "result": result}

        ### 3. Code Explanation Node
        def explain_code(state: GraphState) -> GraphState:
            code = state["input"]
            
            vs = self.embedder.load_vectorstore("faiss_code_index")
            context = self.embedder.search_similar_chunks(code, vs)

            res = self.code_explainer.invoke(user_input=code, context=context)
            
            state["messages"].append(f"Code_Explanation_Agent : \n{res}")
            
            explanation = f"Explanation of the code: {res}"
            return {**state, "result": f"{explanation}"}

        ### 4. Code Refactoring Node
        def refactor_code(state: GraphState) -> GraphState:
            query = state["input"]
            # Directly extract filename from user input using regex
            import re
            match = re.search(r"([\w\-]+\.py)", query)
            filename = match.group(1) if match else None

            print(f"Extracted filename : {filename}")
            refactored = self.refactorer.invoke(filepath=filename, prompt=query)

            if refactored:
                print("succes refactoring")
                print(refactored)
            else:
                print("I dont know why it did not work")
            return {**state, "result": refactored}

        ### 5. Build the Graph
        builder = StateGraph(GraphState)

        builder.add_node("decision", decision_node)
        builder.add_node("explain", RunnableLambda(explain_code))
        builder.add_node("refactor", RunnableLambda(refactor_code))
        builder.add_node("code_search", RunnableLambda(code_search_node))


        # Add Decision Node
        builder.add_conditional_edges(
            "decision", decide_task, {
                "explain": "explain",
                "refactor": "refactor",
                "code_search": "code_search",
            }
        )

        # Route both paths to END
        builder.add_edge("explain", END)
        builder.add_edge("refactor", END)

        # Set entry point
        builder.set_entry_point("decision")

        graph = builder.compile()

        
        self.graph = graph
        return graph

    def run(self, input: str):
        inputs = {"input": input}

        result = self.graph.invoke(inputs)
        print(result["result"])
        return result["result"]

# if __name__ == "__main__":
#     agent = SubAgent()
#     agent.run(input="can you add doctsring to all functions in the main.py file")


