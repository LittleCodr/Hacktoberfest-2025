from github import Github
import random
import os

# Auth and repo setup
token = os.getenv("GITHUB_TOKEN")
email = os.getenv("GITHUB_EMAIL")
repo_name = os.getenv("GITHUB_REPOSITORY")

g = Github(token)
repo = g.get_repo(repo_name)

# ---- Editable values ----
COMMITS = 20
PULL_REQUESTS = 400    # <--- change this number for PRs
CODE_REVIEWS = 250     # <--- change this number for reviews
ISSUES = 150           # <--- change this number for issues
# --------------------------

def simulate_commits():
    print(f"Simulating {COMMITS} commits...")
    file_path = "dummy_file.txt"

    # Check if file exists in repo
    contents = repo.get_contents(file_path)
    sha = contents.sha

    for i in range(COMMITS):
        new_content = contents.decoded_content.decode() + f"\nCommit #{i+1}"
        repo.update_file(
            path=file_path,
            message=f"Commit #{i+1}",
            content=new_content,
            sha=sha
        )
        print(f"✅ Commit #{i+1} pushed.")
        contents = repo.get_contents(file_path)
        sha = contents.sha


def simulate_pull_requests():
    print(f"Simulating {PULL_REQUESTS} pull requests...")
    for i in range(PULL_REQUESTS):
        print(f"🟢 PR simulated #{i+1}")


def simulate_code_reviews():
    print(f"Simulating {CODE_REVIEWS} code reviews...")
    for i in range(CODE_REVIEWS):
        print(f"🟡 Code review simulated #{i+1}")


def simulate_issues():
    print(f"Simulating {ISSUES} issues...")
    for i in range(ISSUES):
        print(f"🔵 Issue simulated #{i+1}")


if __name__ == "__main__":
    simulate_commits()
    simulate_pull_requests()
    simulate_code_reviews()
    simulate_issues()
    print("✅ Daily activity simulation completed successfully!")
