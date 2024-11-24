import os
import subprocess
from datetime import datetime, timedelta


def check_dependencies():
    """Check if GitHub CLI and Git are installed."""
    try:
        subprocess.run(["gh", "--version"], check=True, stdout=subprocess.PIPE)
    except FileNotFoundError:
        print("GitHub CLI (gh) is not installed. Please install it first.")
        exit(1)

    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE)
    except FileNotFoundError:
        print("Git is not installed. Please install it first.")
        exit(1)


def create_repository():
    """Create a new private GitHub repository."""
    repo_name = input("Enter the name for your new repository: ")
    subprocess.run(["gh", "repo", "create", repo_name, "--private", "--confirm"], check=True)
    print(f"Repository '{repo_name}' created successfully.")
    return repo_name


def choose_existing_repository():
    """List existing repositories and let the user choose one."""
    print("Fetching your repositories...")
    repos = subprocess.run(["gh", "repo", "list", "--limit", "100"], stdout=subprocess.PIPE, text=True)
    repo_list = repos.stdout.strip().split("\n")
    for i, repo in enumerate(repo_list, start=1):
        print(f"{i}: {repo.split()[0]}")

    repo_choice = int(input("Enter the number of the repository you want to use: ")) - 1
    repo_name = repo_list[repo_choice].split()[0]
    print(f"Selected repository: {repo_name}")
    return repo_name


def clone_repository(repo_name):
    """Clone the selected repository."""
    # Dynamically fetch the GitHub username
    username = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"], stdout=subprocess.PIPE, text=True
    ).stdout.strip()

    # Construct the repository URL
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    print(f"Cloning repository: {repo_url}")

    # Clone the repository
    subprocess.run(["git", "clone", repo_url], check=True)
    os.chdir(os.path.basename(repo_name))


def generate_commits(start_date):
    """Generate fake commits from a given start date to today."""
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.now()
    current_date = start_date
    commit_time = "12:00:00"  # Default commit time

    while current_date < end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        with open("commit.txt", "w") as f:
            f.write(f"Commit on {date_str}")
        subprocess.run(["git", "add", "commit.txt"], check=True)

        commit_date = f"{date_str} {commit_time}"
        env = os.environ.copy()
        env["GIT_COMMITTER_DATE"] = commit_date
        subprocess.run(
            ["git", "commit", "--date", commit_date, "-m", f"Commit for {date_str}"],
            check=True,
            env=env,
        )
        current_date += timedelta(days=1)

    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("All commits pushed successfully!")


def main():
    """Main script logic."""
    check_dependencies()

    print("Do you want to:")
    print("1. Create a new repository")
    print("2. Use an existing repository")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        repo_name = create_repository()
    elif choice == "2":
        repo_name = choose_existing_repository()
    else:
        print("Invalid choice. Exiting.")
        exit(1)

    clone_repository(repo_name)

    start_date = input("Enter the start date for commits (YYYY-MM-DD): ")
    generate_commits(start_date)


if __name__ == "__main__":
    main()
