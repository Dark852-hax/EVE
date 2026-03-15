"""
Upload EVE to GitHub
"""
import os
import github

# You need a GitHub token with repo scope
# Set it as environment variable GITHUB_TOKEN or edit below
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Get the token from config if not set
if not GITHUB_TOKEN:
    config_path = os.path.join(os.path.dirname(__file__), 'backend', 'config.json')
    if os.path.exists(config_path):
        import json
        with open(config_path) as f:
            config = json.load(f)
            GITHUB_TOKEN = config.get('github', {}).get('token', '')

if not GITHUB_TOKEN or GITHUB_TOKEN == "YOUR_GITHUB_TOKEN_HERE":
    print("ERROR: No GitHub token found!")
    print("Please set GITHUB_TOKEN environment variable or add your token to backend/config.json")
    print("\nTo create a token:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Create new token with 'repo' scope")
    print("3. Add it to config.json: 'github': {'token': 'your_token'}")
    exit(1)

REPO_NAME = "EVE"

# Get the files to upload
eve_dir = os.path.dirname(__file__)
files_to_upload = {}

for root, dirs, files in os.walk(eve_dir):
    # Skip hidden directories and .git
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
    
    for file in files:
        if file.startswith('.') or file.endswith('.pyc'):
            continue
        
        filepath = os.path.join(root, file)
        rel_path = os.path.relpath(filepath, eve_dir)
        
        with open(filepath, 'rb') as f:
            content = f.read()
        
        files_to_upload[rel_path] = content.decode('utf-8', errors='ignore')

print(f"Uploading {len(files_to_upload)} files to GitHub...")

# Connect to GitHub
g = github.Github(GITHUB_TOKEN)

try:
    # Try to get existing repo
    user = g.get_user()
    try:
        repo = user.get_repo(REPO_NAME)
        print(f"Found existing repo: {repo.full_name}")
    except:
        # Create new repo
        print(f"Creating new repository: {REPO_NAME}")
        repo = user.create_repo(
            name=REPO_NAME,
            description="EVE AI - Autonomous General Intelligence Assistant",
            private=False,
            has_wiki=False
        )
        print(f"Created new repo: {repo.full_name}")
    
    # Upload files
    for filepath, content in files_to_upload.items():
        try:
            # Try to get existing file
            contents = repo.get_contents(filepath)
            repo.update_file(
                path=filepath,
                message=f"Update {filepath}",
                content=content,
                sha=contents.sha
            )
            print(f"Updated: {filepath}")
        except:
            # Create new file
            repo.create_file(
                path=filepath,
                message=f"Add {filepath}",
                content=content
            )
            print(f"Created: {filepath}")
    
    print(f"\n✅ Successfully uploaded to https://github.com/{g.get_user().login}/{REPO_NAME}")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nMake sure your token has 'repo' scope permissions")
