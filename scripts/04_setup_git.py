import os
import subprocess
from datetime import datetime

def run_command(command, shell=True):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=shell, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)
    return result

def main():
    # 1. Generate repo name
    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    repo_name = f"project_{current_time}"
    print(f"Repo name: {repo_name}")

    # 2. git init
    run_command("git init")
    run_command("git checkout -b main")

    # 3. Create .gitignore
    with open(".gitignore", "w") as f:
        f.write("src/\n")
        f.write("*.pyc\n")
        f.write("__pycache__/\n")
        f.write("current_notebook_id.txt\n")
    
    # 4. git add and commit
    run_command("git add .")
    run_command('git commit -m "Initial commit - books and structure"')

    # 5. gh repo create
    # Use SSH for remote
    # --public: create public repo
    # --source=.: use current directory
    # --push: push the committed code
    run_command(f"gh repo create {repo_name} --public --source=. --remote=origin --push")

    print(f"Phase 3 complete. Repo: {repo_name}")
    with open("repo_info.txt", "w") as f:
        f.write(repo_name)

if __name__ == "__main__":
    main()
