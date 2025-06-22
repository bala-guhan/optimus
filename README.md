# Multi-Agent Coding Assistant

A multi-agent system designed to boost developer productivity with advanced code explanation, semantic code search, and automated code refactoring.

![Optimus Agent Architecture](./optimus-agent-excalidraw.png)

Built with **LangGraph**, **LangChain**, **FAISS**, **HuggingFace**, and **PostgreSQL** for robust, scalable, and intelligent codebase interaction.

---

## Features

- **Code Explanation:**
  - Get detailed, step-by-step explanations for any code snippet in your codebase.
- **Code Search:**
  - Perform semantic search across your codebase to quickly find relevant code snippets.
- **Code Refactoring:**
  - Automatically refactor code files based on your instructions, leveraging LLM-powered suggestions.
- **Memory Architecture:**
  - Each sub-agent (explanation, search, refactor) has its own episodic memory.
  - The main agent (OptimusPrime) maintains thread-level memory using PostgreSQL for chat history.

---

## Architecture

- **Main Agent:**

  - `optimus_prime.py` — orchestrates sub-agents and manages workflow using LangGraph.

- **Sub-Agents:**

  - Code Explanation Agent
  - Code Search Agent
  - Code Refactoring Agent

- **Technologies Used:**
  - **LangGraph:** For agent workflow and state management.
  - **LangChain:** For LLM integration and file operations.
  - **FAISS:** For fast vector-based semantic search.
  - **HuggingFace (all-MiniLM-L6-v2):** For code embeddings.
  - **Ollama (Llama 3):** For LLM-powered tasks (must be running on the host).
  - **PostgreSQL:** For persistent chat/thread memory.

---

## Setup & Usage

<!-- Add setup, installation, and usage instructions here. -->
