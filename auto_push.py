import subprocess
from pathlib import Path

def push_to_github(repo_path):
    repo = Path(repo_path)

    # git add .
    subprocess.run(["git", "add", "."], cwd=repo)

    # git commit -m "update"
    subprocess.run(["git", "commit", "-m", "auto update"], cwd=repo)

    # git push
    subprocess.run(["git", "push"], cwd=repo)

if __name__ == "__main__":
    push_to_github("D:/ScreenerGIT/Screener")
