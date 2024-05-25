import os
import shutil
from pathlib import Path
import requests
import git
import magika

m = magika.Magika()

# The GitHub repository URL
repo_url = "https://github.com/GoogleCloudPlatform/microservices-demo"  # @param {type:"string"}

# The location to clone the repo
repo_dir = "../repo"


def clone_repo(repo_url, repo_dir):
    """Clone a GitHub repository."""

    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir)
    git.Repo.clone_from(repo_url, repo_dir)


def extract_code(repo_dir):
    """Create an index, extract content of code/text files."""

    code_index = []
    code_text = ""
    for root, _, files in os.walk(repo_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_dir)
            code_index.append(relative_path)

            file_type = m.identify_path(Path(file_path))
            if file_type.output.group in ("text", "code"):
                try:
                    with open(file_path, "r") as f:
                        code_text += f"----- File: {relative_path} -----\n"
                        code_text += f.read()
                        code_text += "\n-------------------------\n"
                except Exception:
                    pass

    return code_index, code_text


def get_github_issue(owner: str, repo: str, issue_number: str) -> str:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }  # Set headers for GitHub API

    # Construct API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    try:
        response_git = requests.get(url, headers=headers)
        response_git.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as error:
        print(f"Error fetching issue: {error}")  # Handle potential errors

    issue_data = response_git.json()
    if issue_data:
        return issue_data["body"]
    return ""


def get_code_prompt(question, code_index, code_text):
    """Generates a prompt to a code related question."""

    prompt = f"""
    Questions: {question}

    Context:
    - The entire codebase is provided below.
    - Here is an index of all of the files in the codebase:
      \n\n{code_index}\n\n.
    - Then each of the files is concatenated together. You will find all of the code you need:
      \n\n{code_text}\n\n

    Answer:
  """

    return prompt


clone_repo(repo_url, repo_dir)
