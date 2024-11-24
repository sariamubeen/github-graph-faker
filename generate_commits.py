import os
import shutil
import subprocess
from datetime import datetime, timedelta


def colorful_text(text, color_code):
    """Return text with ANSI color codes."""
    return f"\033[{color_code}m{text}\033[0m"


def show_welcome():
    """Display the welcome view."""
    print("=" * 50)
    print(colorful_text("Welcome to the GitHub Contribution Faker Tool", "36"))  # Cyan
    print(colorful_text("Created by: Saria Mubeen", "33"))  # Yellow
    print(colorful_text("Description: Generate commits to make your GitHub graph green!", "32"))  # Green
    print(colorful_text("Press Ctrl+C or type 'quit' to exit at any time.", "31"))  # Red
    print("=" * 50)
    print()


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
    if repo_name == "0":
        return None
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

    print("0: Go back to the main menu")
    while True:
        repo_choice = input("Enter the number of the repository you want to use: ")
        if repo_choice == "0":  # Handle the main menu option
            return None
        if repo_choice.isdigit() and 1 <= int(repo_choice) <= len(repo_list):
            repo_name = repo_list[int(repo_choice) - 1].split()[0]
            print(f"Selected repository: {repo_name}")
            return repo_name
        else:
            print("Invalid input. Please enter a valid number.")


def clone_repository(repo_name):
    """Clone the selected repository."""
    # Dynamically fetch the GitHub username
    username = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"], stdout=subprocess.PIPE, text=True
    ).stdout.strip()

    # Construct the repository URL
    repo_url = f"https://github.com/{repo_name}.git"
    print(f"Cloning repository: {repo_url}")

    # Check if the directory already exists
    repo_dir = os.path.basename(repo_name)
    if os.path.exists(repo_dir):
        print(f"Directory '{repo_dir}' already exists.")
        while True:
            choice = input("Do you want to (1) use the existing directory or (2) overwrite it? Enter your choice (1/2): ")
            if choice == "1":
                print(f"Using the existing directory: {repo_dir}")
                os.chdir(repo_dir)
                return
            elif choice == "2":
                print(f"Overwriting the directory: {repo_dir}")
                shutil.rmtree(repo_dir)  # Cross-platform directory removal
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    # Clone the repository
    subprocess.run(["git", "clone", repo_url], check=True)
    os.chdir(repo_dir)


def generate_commits(start_date, end_date):
    """Generate fake commits from a given start date to the end date."""
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    current_date = start_date
    commit_time = "12:00:00"  # Default commit time

    while current_date <= end_date:
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
    while True:
        try:
            show_welcome()
            check_dependencies()

            print("Do you want to:")
            print("1. Create a new repository")
            print("2. Use an existing repository")
            print("0. Go back to the main menu")
            choice = input("Enter your choice (1/2/0): ")

            if choice == "0":
                continue
            elif choice == "1":
                repo_name = create_repository()
                if repo_name is None:
                    continue
            elif choice == "2":
                repo_name = choose_existing_repository()
                if repo_name is None:
                    continue
            else:
                print("Invalid choice. Exiting.")
                continue

            clone_repository(repo_name)

            start_date = input("Enter the start date for commits (YYYY-MM-DD): ")
            end_date = input("Enter the end date for commits (YYYY-MM-DD or press Enter for today): ")
            if not end_date.strip():
                end_date = datetime.now().strftime("%Y-%m-%d")  # Default to today

            generate_commits(start_date, end_date)
        except KeyboardInterrupt:
            print("\nExiting the tool. Thank you for using the GitHub Contribution Faker Tool!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
