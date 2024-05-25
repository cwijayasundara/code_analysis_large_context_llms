import os
from dotenv import load_dotenv
import vertexai

from vertexai.generative_models import (
    GenerativeModel,
)

from util.util import extract_code, get_code_prompt

load_dotenv()

# The location to clone the repo
repo_dir = "../repo"

PROJECT_ID = os.environ["PROJECT_ID"]
REGION = os.environ["REGION"]

vertexai.init(project=PROJECT_ID, location=REGION)

MODEL_ID = "gemini-1.5-pro-preview-0514"

model = GenerativeModel(
    MODEL_ID,
    system_instruction=[
        "You are a coding expert.",
        "Your mission is to answer all code related questions with given context and instructions.",
    ],
)

code_index, code_text = extract_code(repo_dir)

question = """
  Find the most severe bug in the codebase that you can provide a code fix for.
"""

prompt = get_code_prompt(question, code_index, code_text)
contents = [prompt]

responses = model.generate_content(contents, stream=True)
for response in responses:
    print(response.text)
