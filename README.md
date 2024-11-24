
# GitHub Graph Faker

This Python script helps you generate fake GitHub commits to make your GitHub contribution graph fully green! You can create commits for specific dates, ensuring your contribution graph looks active.

## Features
- Automatically create or use an existing repository.
- Generate daily commits starting from a user-specified date.
- Push all commits to your GitHub repository.
- Works on Windows, Linux, and macOS.

## Prerequisites
Before running the script, ensure the following tools are installed:
1. [Python](https://www.python.org/downloads/)
2. [Git](https://git-scm.com/downloads)
3. [GitHub CLI (`gh`)](https://cli.github.com/)

You must also authenticate `gh` with your GitHub account:
```bash
gh auth login
```

## Usage

### Step 1: Clone this Repository
```bash
git clone https://github.com/sariamubeen/github-graph-faker.git
cd github-graph-faker
```

### Step 2: Run the Script
Run the script using Python:
```bash
python generate_commits.py
```

### Step 3: Follow the Prompts
1. Choose to either create a new repository or use an existing one.
2. If creating a new repository, enter the desired name (e.g., `my-contributions`).
3. Enter the start date for your commits (format: `YYYY-MM-DD`).
4. Sit back as the script generates commits for every day starting from the given date!

### Step 4: Check Your Contribution Graph
After the script finishes, visit your [GitHub profile](https://github.com/) to view the updated contribution graph. It may take a few minutes to reflect the changes.

## Example
Here’s how to generate commits starting from January 1, 2023:
```bash
python generate_commits.py
```
When prompted:
- Choose "Create a new repository" and name it `my-contribution-graph`.
- Enter the start date as `2023-01-01`.

The script will generate daily commits from January 1, 2023, to today.

## Script Details

### Dependencies
The script requires the following Python libraries (available in the standard library):
- `os`
- `subprocess`
- `datetime`

### Functionality
1. **Check Dependencies**:
   Verifies that `gh` and `git` are installed.
2. **Create or Use Repository**:
   Allows you to create a new private repository or choose an existing one.
3. **Generate Commits**:
   Automates the creation of commits for each day starting from the user-defined date.
4. **Push to GitHub**:
   Pushes the commits to your repository's `main` branch.

## Troubleshooting
If the script runs but your graph doesn’t update:
1. **Ensure Your Git Email Matches Your GitHub Account**:
   ```bash
   git config --global user.email "your-email@example.com"
   ```
   Replace `"your-email@example.com"` with the email associated with your GitHub account.

2. **Commits Not on Default Branch**:
   Ensure commits are pushed to the `main` branch.

3. **Private Repository Contributions**:
   Contributions from private repositories only appear on your graph if the repository is owned by you.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute.

---

Enjoy building an awesome-looking contribution graph! 😊
