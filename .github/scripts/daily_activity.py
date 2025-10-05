#!/usr/bin/env python3
# .github/scripts/daily_activity.py
# Runs inside GitHub Actions. Uses PyGithub.

import os
import random
import time
import uuid
import sys
from github import Github
from datetime import datetime, timezone

GH_TOKEN = os.environ.get("GH_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME", "LittleCodr/profile-booster")

if not GH_TOKEN:
    print("ERROR: GH_TOKEN not found in environment.")
    sys.exit(1)

g = Github(GH_TOKEN)
repo = g.get_repo(REPO_NAME)

# Total actions today: random between 50 and 60
total_actions = random.randint(50, 60)
print(f"Running {total_actions} actions on {REPO_NAME}")

created_pr_numbers = []

for i in range(total_actions):
    action = random.choices(["pr", "issue", "review"], weights=[0.5, 0.3, 0.2], k=1)[0]
    try:
        if action == "pr":
            # create a new branch and file, then a PR
            ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            shortid = uuid.uuid4().hex[:6]
            branch_name = f"auto/pr/{ts}/{shortid}"
            source = repo.get_branch(repo.default_branch)
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)

            file_path = f"auto_pr_files/{shortid}_{ts}.md"
            content = f"# Auto PR\nThis PR was auto-generated at {datetime.now(timezone.utc).isoformat()} UTC\n"
            repo.create_file(path=file_path, message=f"Add {file_path}", content=content, branch=branch_name)

            pr = repo.create_pull(
                title=f"Auto PR {ts}-{shortid}",
                body=f"Auto-generated PR {i}",
                head=branch_name,
                base=repo.default_branch,
            )
            created_pr_numbers.append(pr.number)
            print(f"[{i+1}/{total_actions}] Created PR #{pr.number}")

        elif action == "issue":
            issue = repo.create_issue(
                title=f"Auto Issue #{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{i}",
                body=f"Auto-generated issue {i} at {datetime.now(timezone.utc).isoformat()} UTC",
            )
            print(f"[{i+1}/{total_actions}] Created Issue #{issue.number}")

        else:  # review
            pulls = list(repo.get_pulls(state="open"))
            if not pulls:
                # create a tiny PR to have something to review
                ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
                shortid = uuid.uuid4().hex[:6]
                branch_name = f"auto/pr/{ts}/{shortid}"
                source = repo.get_branch(repo.default_branch)
                repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
                file_path = f"auto_pr_files/{shortid}_{ts}.md"
                repo.create_file(path=file_path, message=f"Add {file_path}", content="Temp PR for review", branch=branch_name)
                pr = repo.create_pull(title=f"Auto PR for review {ts}", body="temp", head=branch_name, base=repo.default_branch)
                pulls = [pr]
                print(f"[{i+1}/{total_actions}] Created PR #{pr.number} (for review)")

            pr = random.choice(pulls)
            event = random.choice(["APPROVE", "COMMENT", "REQUEST_CHANGES"])
            pr.create_review(body=f"Auto review {i} - {event}", event=event)
            print(f"[{i+1}/{total_actions}] Created review on PR #{pr.number} event={event}")

    except Exception as e:
        print(f"[{i+1}/{total_actions}] ERROR doing {action}: {e}")

    # small random delay to avoid huge bursts
    time.sleep(random.uniform(0.5, 1.5))

print("Done. Actions created:", total_actions)
