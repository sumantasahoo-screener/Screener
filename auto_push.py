import os
import subprocess

def push_to_github(repo_path):
    try:
        os.chdir(repo_path)

        # Add EVERYTHING inside public folder
        subprocess.run(["git", "add", "public/"], check=True)

        # Commit (will include add / modify / delete)
        subprocess.run(
            ["git", "commit", "-m", "Auto push public folder"],
            check=True
        )

        # Push to GitHub
        subprocess.run(["git", "push"], check=True)

        print("✅ Public folder pushed successfully")

    except subprocess.CalledProcessError as e:
        print("❌ Git command failed:", e)

    except Exception as e:
        print("❌ Unexpected error:", e)
