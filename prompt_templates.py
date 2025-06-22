from langchain.prompts import ChatPromptTemplate
from tools import read_file
import traceback

code_refactor_prompt_template_1 = ChatPromptTemplate.from_template(
    """
Here is a code section from the file: {filename}

User's refactor prompt:
{user_prompt}

Code section:
{code_section}

Please carefully analyze the code and the file content. Based on your analysis, make a decision:

(a) If the code can be fixed within this file itself, say:
"The code can be fixed within this file itself."

(b) If the code uses imports from other project modules (not standard libraries), and those modules could be affected, say:
"Other files could be affected by this piece of code, so I would like to scan the code base for other files."

Only check for imports from other modules in the project (not standard libraries or external packages). Output only a single-line decision as described above.
"""
)

# filename = "../codebase/main.py"
# user_prompt = "can you fix the error in this bubble sort please"

# try:
#     code_section = read_file.invoke({"filepath" : filename})
#     print(code_section)
# except Exception as e:
#     print(traceback.print_exc(e))
    
