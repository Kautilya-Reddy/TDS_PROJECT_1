import os
import time
import requests

# Load token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
GITHUB_API = "https://api.github.com"

def _headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

def create_repo(name, private=False):
    """Create a new GitHub repository."""
    url = f"{GITHUB_API}/user/repos"
    data = {
        "name": name,
        "description": "Auto-generated repository for IITM LLM Deployment project",
        "private": private,
        "auto_init": True,
    }

    r = requests.post(url, headers=_headers(), json=data)
    if r.status_code == 201:
        repo = r.json()
        print(f"✅ Repository created: {repo['name']}")
        return repo
    else:
        print(f"❌ Failed to create repo: {r.status_code}, {r.text}")
        return None


def upload_file(repo_full_name, path, content, message="Auto-upload"):
    """Create or update a file in the repository."""
    url = f"{GITHUB_API}/repos/{repo_full_name}/contents/{path}"
    data = {
        "message": message,
        "content": content.encode("utf-8").decode("utf-8") if isinstance(content, str) else content,
        "branch": "main"
    }

    # Convert text to base64 (GitHub API requirement)
    import base64
    data["content"] = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    r = requests.put(url, headers=_headers(), json=data)
    if r.status_code in [201, 200]:
        print(f"✅ Uploaded file: {path}")
    else:
        print(f"❌ Upload failed for {path}: {r.status_code}, {r.text}")


def enable_pages(repo_full_name):
    """Enable GitHub Pages with retries for reliability."""
    url = f"{GITHUB_API}/repos/{repo_full_name}/pages"
    data = {"source": {"branch": "main"}}

    for attempt in range(3):
        try:
            r = requests.post(url, headers=_headers(), json=data, timeout=15)
            if r.status_code in [201, 204]:
                print(f"🌐 GitHub Pages enabled for {repo_full_name}")
                owner, repo = repo_full_name.split("/")
                return f"https://{owner}.github.io/{repo}/"
            else:
                print(f"⚠️ Attempt {attempt+1}: Could not enable GitHub Pages ({r.status_code}). Retrying...")
                time.sleep(5)
        except requests.exceptions.Timeout:
            print(f"⏳ Attempt {attempt+1}: GitHub API timed out, retrying...")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Attempt {attempt+1}: Unexpected error enabling Pages: {e}")
            time.sleep(5)

    print(f"❌ Failed to enable GitHub Pages after multiple attempts.")
    return None


def get_user_info():
    """Check token validity and return user info."""
    url = f"{GITHUB_API}/user"
    r = requests.get(url, headers=_headers())
    if r.status_code == 200:
        return r.json()
    else:
        print(f"❌ Authentication failed: {r.status_code}, {r.text}")
        return None
