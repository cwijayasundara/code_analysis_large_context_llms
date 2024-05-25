import os
from dotenv import load_dotenv
import vertexai
import streamlit as st

from vertexai.generative_models import (
    GenerativeModel,
)

from util.util import extract_code, get_code_prompt

load_dotenv()

# The location to clone the repo
repo_dir = "./repo"

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

options = ["Give me a summary of this codebase, and tell me the top 3 things that I can learn from it",
           "Provide a getting started guide to onboard new developers to the codebase",
           "Find the top 3 most severe issues in the codebase",
           "Find the most severe bug in the codebase that you can provide a code fix for",
           "Provide a class diagram in Mermaid format for the following code",
           "How can I make this application more reliable? Consider best practices from https://www.r9y.dev/",
           ]

st.title("Source Code Analyzer !")

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image("images/code_analyser.webp")

manual_mode = st.checkbox("manual mode")
if manual_mode:
    code_analysis_query = st.text_input("How can I help you today?")
    submit = st.button("submit", type="primary")
    if code_analysis_query and submit:
        prompt = get_code_prompt(code_analysis_query, code_index, code_text)
        print("the prompt used is", prompt)
        contents = [prompt]
        response = model.generate_content(contents)
        st.write(response.text)
else:
    option = st.selectbox('Code Analyzer Query !!', options)
    submit = st.button("submit", type="primary")
    if option and submit:
        prompt = get_code_prompt(option, code_index, code_text)
        print("the manual prompt used is", prompt)
        contents = [prompt]
        response = model.generate_content(contents)
        st.write(response.text)
