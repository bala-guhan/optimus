from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from tools import read_file, read_file_lines, write_file_lines, find_file_in_codebase, apply_code_replacements
from typing import Optional, List
from pydantic import BaseModel, Field
import json
from langchain.output_parsers import PydanticOutputParser

load_dotenv()


class Refactor:
    def __init__(self, model) -> None:
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.model = model
        self.chat_history = []
        self.output_structure = None
        self.set_output_structure()

    def set_output_structure(self):
        class CodeReplacement(BaseModel):
            old_code: str
            new_code: str

        class MultipleReplacements(BaseModel):
            changes: List[CodeReplacement]
        
        self.output_structure = MultipleReplacements
        
    def invoke(self, filepath: str, prompt: str, code_selection: str = Optional):
        """single file changes LLM Chain"""

        filename = find_file_in_codebase.invoke(filepath)
        print("here is the filename after tool call" ,filename)

        file_content = read_file.invoke({"filepath" : filename})
        self.chat_history.append({"role" : "tool", "message" : file_content})
        
        if file_content:
            print("file read successfully")
        else:
            print("error reading file")
            return 

        prompt_template = ChatPromptTemplate.from_template("""
        System: You are a code refactoring agent.

        You are given:
        - The entire file content : {file_content}
        - The user's input prompt : {prompt}

        Your task:
        - Analyze the code and refactor it according to the user's prompt and the whole file content.
        - For each change, output the old code block (exactly as it appears in the file) and the new code block to replace it with.

        **Output Format:**
        Return a JSON object with a "changes" key, whose value is a list of objects, each with the following fields:
        - "old_code": The exact code block to be replaced (as it appears in the file)
        - "new_code": The new code block to replace it with

        Example:
        {{
          "changes": [
            {{
              "old_code": "...",
              "new_code": "..."
            }}
          ]
        }}

        **Instructions:**
        - Only output valid JSON matching the above format.
        - For each change, ensure "old_code" matches exactly what is in the file.
        - If no change is needed, return {{"changes": []}}
        """)
        
        parser = PydanticOutputParser(pydantic_object=self.output_structure)
        chain = prompt_template | self.model
        raw_res = chain.invoke({"filename": filepath, 
                      "prompt": prompt,
                      "file_content": file_content, 
                      })
        # Use the parser to parse the output
        try:
            if hasattr(raw_res, 'content'):
                output_text = raw_res.content
            else:
                output_text = str(raw_res)
            res = parser.parse(output_text)
        except Exception as e:
            print("Error parsing model output as structured data:", e)
            print("Raw output was:", raw_res)
            return {"error": "Failed to parse model output as structured data", "raw_output": output_text}
        
        if not res.changes:
            print("No changes to apply")
            return {"result" : "No Changes needed"}
        
        # Convert CodeReplacement objects to dicts for JSON serialization
        changes_as_dicts = [item.dict() for item in res.changes]
        with open('output.txt', 'w') as file:
            for item in changes_as_dicts:
                file.write(item['old_code'])
                file.write("-----"*10)
                file.write(item['new_code'])
        try:
            result = apply_code_replacements.invoke({"file_path": filename, "replacements": changes_as_dicts})
            print("Code replacements applied successfully!")
            return {"changes": changes_as_dicts, "result": "success"}
        except Exception as e:
            print("Error applying code replacements:", e)
            print(res)
            return {"error": str(e)}

# exp = Refactor()
# output = exp.invoke(filepath='../codebase/main.py', prompt="add docstrings to all the functions present in the main.py file")


