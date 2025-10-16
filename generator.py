from github_utils import create_repo, upload_file, enable_pages
import random
import time

def generate_app(task_name, brief=None):
    # Create a unique repo name
    repo_name = f"{task_name}-{random.randint(1000,9999)}"
    repo_data = create_repo(repo_name)

    if not repo_data:
        print("❌ Could not create repository.")
        return None

    repo_full_name = repo_data["full_name"]

    # Step 1: Generate simple app HTML (you can expand this later for different briefs)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{task_name} App</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
        <div class="container text-center">
            <h1 class="mb-4">GitHub User Lookup</h1>
            <input id="username" class="form-control mb-3" placeholder="Enter GitHub username">
            <button class="btn btn-primary" onclick="fetchUser()">Fetch</button>
            <p class="mt-3" id="github-created-at"></p>
            <p class="text-muted" id="status"></p>
        </div>
        <script>
            async function fetchUser() {{
                const name = document.getElementById('username').value;
                const status = document.getElementById('status');
                status.textContent = 'Fetching...';
                try {{
                    const res = await fetch(`https://api.github.com/users/${{name}}`);
                    const data = await res.json();
                    if (data.created_at) {{
                        document.getElementById('github-created-at').textContent = 
                            'Account created on: ' + new Date(data.created_at).toISOString().split('T')[0];
                        status.textContent = 'Success!';
                    }} else {{
                        status.textContent = 'User not found.';
                    }}
                }} catch (e) {{
                    status.textContent = 'Error fetching data.';
                }}
            }}
        </script>
    </body>
    </html>
    """

    # Step 2: Upload core files
    upload_file(repo_full_name, "index.html", html_content)
    upload_file(repo_full_name, "README.md", f"# {task_name}\n\n{brief or 'Auto-generated web app.'}")
    upload_file(repo_full_name, "LICENSE", "MIT License")

    # Step 3: Enable GitHub Pages
    print("⏳ Waiting for GitHub to settle before enabling Pages...")
    time.sleep(3)
    pages_url = enable_pages(repo_full_name)

    print("✅ Deployment completed successfully!")
    print("🌐 Pages URL:", pages_url)

    return {
        "repo_url": repo_data["html_url"],
        "commit_sha": repo_data["default_branch"],
        "pages_url": pages_url
    }
